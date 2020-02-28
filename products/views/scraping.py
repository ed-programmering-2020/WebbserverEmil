from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import generics
from operator import itemgetter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from difflib import SequenceMatcher
from django.db.models import Q
from products.models import Product, Website, BaseCategoryProduct, BaseSpecification, AlternativeCategoryName
import string
import json


class ProductsAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data_list = json.loads(request.data.get("products"))
        files_list = request.FILES

        for product_data in data_list:
            product = self.create_or_get_product(product_data, files_list)

            # Get matching meta-product/product
            matching_product = self.find_matching_product(product)
            if matching_product:
                category_product = self.combine_products(product, matching_product)
            else:
                matching_category_product = self.find_matching_category_product(product)

                if matching_category_product:
                    product.category_product = matching_category_product

                category_product = product.category_product

            # Update product
            if category_product:
                category_product.update()

        return Response({})

    def create_or_get_product(self, data, files_dict):
        url = data.get("link")
        host = Website.objects.get(name=data.get("website"))
        manufacturing_name = data.get("manufacturing_name")

        # Create/get product
        product = Product.objects.filter(Q(url=url) | Q(manufacturing_name=manufacturing_name), Q(host=host)).first()
        if not product:
            filename = data.get("image")
            image = files_dict.get(filename) if filename else None
            product = Product(
                name=data.get("title"),
                url=url,
                host=host,
                image=image,
                category=data.get("category"),
                manufacturing_name=manufacturing_name
            )
            product.specifications = data.get("specs")

        # Overall update
        product.save()
        product.price = data.get("price")

        return product

    def find_matching_product(self, product):
        if product.manufacturing_name:
            try:
                return Product.objects \
                    .exclude(id=product.id) \
                    .get(manufacturing_name=product.manufacturing_name)
            except Product.DoesNotExist:
                return None
        else:
            return None

    def find_matching_category_product(self, product):
        category_products = BaseCategoryProduct.objects.all()
        matching_products = []

        name = self.clean_string(product.name)
        specs = product.specifications
        price = product.price
        min_price = price / 2.5
        max_price = price * 2.5

        for category_product in category_products.iterator():
            if not category_product.manufacturing_name or not product.manufacturing_name:

                # Check if price is acceptable and specs match
                prices = [product.price for product in category_product.products]
                average_price = (sum(prices) / len(prices)) / 2

                if min_price <= average_price <= max_price and self.matching_specs(specs, category_product):
                    # Get top meta-product name similarity
                    names = [self.clean_string(product.name) for product in category_product.products]
                    name_similarity = self.name_similarity(name, names)
                    matching_products.append((name_similarity, product))

        # Return top meta product that is over the threshold
        if len(matching_products) != 0:
            top_product = max(matching_products, key=itemgetter(0))
            name_similarity, product_id = top_product

            return product_id if name_similarity >= 0.85 else None
        else:
            return None

    def name_similarity(self, name, names):
        similarity_list = []

        for meta_name in names:
            # Get similarities
            sequence_sim = SequenceMatcher(None, name, meta_name).ratio()
            cosine_sim = self.name_similarity_with_cosine(name, meta_name)

            # Add highest similarity
            top_similarity = max([sequence_sim, cosine_sim])
            similarity_list.append(top_similarity)

        return max(similarity_list)

    def name_similarity_with_cosine(self, first_name, second_name):
        names = [first_name, second_name]
        vectorizer = CountVectorizer().fit_transform(names)
        vectors = vectorizer.toarray()

        return self.cosine_sim_vectors(vectors[0], vectors[1])

    def cosine_sim_vectors(self, vec1, vec2):
        vec1 = vec1.reshape(1, -1)
        vec2 = vec2.reshape(1, -1)
        return cosine_similarity(vec1, vec2)[0][0]

    def matching_specs(self, specs, product):
        specifications = BaseSpecification.get_specification_instances(specs)

        for specification in specifications:
            specification_attribute_name = specification.get_attribute_like_name

            if hasattr(specification, specification_attribute_name):
                product_specification = getattr(product, specification_attribute_name)

                if product_specification.id != specification.id:
                    return False

        return True

    def clean_string(self, text):
        text = "".join([word for word in text if word not in string.punctuation])
        text.lower()
        return text

    def combine_products(self, first, second):
        first_category_product = first.category_product
        second_category_product = second.category_product

        if first_category_product and second_category_product:
            category_product = first_category_product

            first_query_set = category_product.products.all()
            second_query_set = second_category_product.products.all()
            combined_query_set = first_query_set.union(second_query_set)

            category_product.products.set(combined_query_set)
            second_category_product.delete()

        elif first_category_product:
            category_product = first_category_product
            category_product.products.add(second)

        elif second_category_product:
            category_product = second_category_product
            category_product.products.add(first)

        elif first.category or second.category:
            if first.category:
                category_name = first.category
            else:
                category_name = second.category

            try:
                AlternativeCategoryName.objects.get(name=category_name)
                category_product_type = AlternativeCategoryName.category_product_type

                if category_product_type is not None:
                    category_product_model = category_product_type.get_model()
                    category_product = category_product_model.objects.create(category_product_type=category_product_type)
                    category_product.products.set([first, second])
                else:
                    return None
            except AlternativeCategoryName.DoesNotExist:
                AlternativeCategoryName.objects.create(name=category_name)
                return None
        else:
            return None

        category_product.save()
        return category_product
