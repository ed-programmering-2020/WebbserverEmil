from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import generics
from operator import itemgetter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from difflib import SequenceMatcher
from django.db.models import Q
from products.models import Product, Website, BaseCategoryProduct
import string
import json


class ProductsAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        self.data_list = json.loads(request.data.get("products"))
        self.files_list = request.FILES

        for product_data in self.data_list:
            meta_product = self.create_or_get_meta_product(product_data)

            # Get matching meta-product/product
            matching_meta_product = self.find_matching_product(meta_product)
            if matching_meta_product:
                product = self.combine_meta_products(meta_product, matching_meta_product)
            else:
                matching_product = self.find_matching_category_product(meta_product)

                if matching_product:
                    meta_product.product = matching_product

                product = meta_product.product

            # Update product
            if product:
                product.update()

        return Response({})

    def create_or_get_meta_product(self, data):
        url = data.get("link")
        host = Website.objects.get(name=data.get("website"))
        manufacturing_name = data.get("manufacturing_name")

        # Create/get product
        product = Product.objects.filter(Q(url=url) | Q(manufacturing_name=manufacturing_name), Q(host=host)).first()
        if not product:
            filename = data.get("image")
            image = self.files_dict.get(filename) if filename else None
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
        product.price = data.get("price")
        product.save()

        return product

    def find_matching_product(self, meta_product):
        if meta_product.manufacturing_name:
            try:
                return Product.objects \
                    .exclude(id=meta_product.id) \
                    .get(manufacturing_name=meta_product.manufacturing_name)
            except Product.DoesNotExist:
                return None
        else:
            return None

    def find_matching_category_product(self, meta_product):
        products = BaseCategoryProduct.objects.all()
        matching_products = []

        price = meta_product.get_price()
        min_price = price / 2.5
        max_price = price * 2.5

        specs = meta_product.get_specs()

        name = self.clean_string(meta_product.name)

        for product in products.iterator():
            if not product.manufacturing_name or not meta_product.manufacturing_name:
                # Check if price is acceptable and specs match
                prices = [meta_product.get_price() for meta_product in product.meta_products]
                average_price = (sum(prices) / len(prices)) / 2

                if min_price <= average_price <= max_price and self.matching_specs(specs, product.spec_values.all()):
                    # Get top meta-product name similarity
                    names = [self.clean_string(meta_product.name) for meta_product in product.meta_products]
                    name_similarity = self.name_similarity(name, names)
                    matching_products.append((name_similarity, meta_product))

        # Return top meta product that is over the threshold
        if len(matching_products) != 0:
            top_meta_product = max(matching_products, key=itemgetter(0))
            name_similarity, product_id = top_meta_product

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

    def matching_specs(self, meta_specs, spec_values):
        for meta_spec in meta_specs:
            key, value = meta_spec

            try:
                spec_key = SpecKey.objects.get(key__iexact=key)
                spec_group = spec_key.spec_group
                value = spec_group.process_value(value)

                if spec_group and spec_group.is_ranked:
                    for spec_value in spec_values:
                        spec_value_group = spec_value.spec_key.spec_group

                        if spec_group.id == spec_value_group.id and value != spec_value.value:
                            return False

            except SpecKey.DoesNotExist:
                pass

        return True

    def clean_string(self, text):
        text = "".join([word for word in text if word not in string.punctuation])
        text.lower()
        return text

    def combine_meta_products(self, first_meta_product, second_meta_product):
        first_product = first_meta_product.product
        second_product = second_meta_product.product

        if first_product and second_product:
            product = first_product

            first_query_set = product.meta_products.all()
            second_query_set = second_product.meta_products.all()
            combined_query_set = first_query_set.union(second_query_set)

            product.meta_products.set(combined_query_set)
            second_product.delete()

        elif first_product:
            product = first_product
            product.meta_products.add(second_meta_product)

        elif second_product:
            product = second_product
            product.meta_products.add(first_meta_product)

        else:
            product = Product.objects.create()
            product.meta_products.set([first_meta_product, second_meta_product])

        product.save()
        return product
