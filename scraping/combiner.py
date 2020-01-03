from django.core.exceptions import ObjectDoesNotExist
from operator import itemgetter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from difflib import SequenceMatcher
from products.models import MetaProduct, Product
from .models import Website
import string


class Combiner:
    def __init__(self, data_list, files_dict):
        self.data_list = data_list
        self.files_dict = files_dict

        for product_data in self.data_list:
            meta_product = self.create_or_get_meta_product(product_data)
            meta_product.update(product_data)

            matching_meta_product = self.find_matching_meta_product(meta_product)
            if matching_meta_product:
                product = self.combine_meta_products(meta_product, matching_meta_product)
            else:
                product = meta_product.product

            if product:
                product.update()

    def create_or_get_meta_product(self, data):
        website = data.get("website")
        filename = data.get("filename")
        image = self.files_dict.get(filename) if filename else None

        try:
            meta_product = MetaProduct.objects.get(url=website)
        except ObjectDoesNotExist:
            meta_product = MetaProduct(
                name=data.get("title"),
                url=website,
                host=Website.objects.get(id=data.get("host_id")),
                image=image
            )

        return meta_product

    def find_matching_meta_product(self, meta_product):
        matching_meta_product = self.match_with_manufacturing_name(meta_product)
        if matching_meta_product is None:
            matching_meta_product = self.match_with_probability(meta_product)

        return matching_meta_product

    def match_with_manufacturing_name(self, meta_product):
        if meta_product.manufacturing_name:
            try:
                return MetaProduct.objects.exclude(id=meta_product.id).get(manufacturing_name=meta_product.manufacturing_name)
            except ObjectDoesNotExist:
                return None
        else:
            return None

    def match_with_probability(self, main_meta_product):
        min_price, max_price = self.acceptable_price_span(main_meta_product)
        meta_products = MetaProduct.objects.exclude(id=main_meta_product.id).filter(price__lte=max_price, price__gte=min_price).all()

        meta_products_with_probability = []
        for meta_product in meta_products.iterator():
            name_similarity = self.name_similarity(main_meta_product.name, meta_product.name)
            parameter_similarity = self.parameter_similarity(main_meta_product.specs, meta_product.specs)

            average_similarity = (name_similarity + parameter_similarity) / 2
            meta_products_with_probability.append((average_similarity, meta_product))

        top_meta_product = max(meta_products_with_probability, key=itemgetter(1))
        return top_meta_product[1] if top_meta_product[0] >= 0.8 else None

    def acceptable_price_span(self, meta_product):
        if meta_product.product:
            prices = [meta_product.get_price() for meta_product in meta_product.product.meta_products]
            price = sum(prices) / len(prices)
        else:
            price = meta_product.get_price()

        min_price = price / 2.5
        max_price = price * 2.5
        return min_price, max_price

    def name_similarity(self, first_name, second_name):
        first_name = self.clean_string(first_name)
        second_name = self.clean_string(second_name)

        sequence_similarity = SequenceMatcher(None, first_name, second_name).ratio()
        cosine_similarity = self.name_similarity_with_cosine(first_name, second_name)
        top_similarity = max([sequence_similarity, cosine_similarity])

        return top_similarity

    def name_similarity_with_cosine(self, first_name, second_name):
        names = [first_name, second_name]
        vectorizer = CountVectorizer().fit_transform(names)
        vectors = vectorizer.toarray()

        return self.cosine_sim_vectors(vectors[0], vectors[1])

    def cosine_sim_vectors(self, vec1, vec2):
        vec1 = vec1.reshape(1, -1)
        vec2 = vec2.reshape(1, -1)
        return cosine_similarity(vec1, vec2)[0][0]

    def parameter_similarity(self, first_params, second_params):
        combined_score = 0
        intersecting_params = 0

        for param in second_params:
            second_key = self.clean_string(param.key)
            second_value = self.clean_string(param.value)

            for first_key, first_value in first_params.items():
                first_key = self.clean_string(first_key)
                first_value = self.clean_string(first_value)

                # Value match
                if second_value in first_value or first_value in second_value:
                    combined_score += 1
                    intersecting_params += 1
                    break

                # Check if params match
                key_similarity = SequenceMatcher(None, first_key, second_key).ratio()
                value_similarity = SequenceMatcher(None, first_value, second_value).ratio()

                if key_similarity >= 0.9 or value_similarity >= 0.9:
                    intersecting_params += 1
                    break

        return combined_score / intersecting_params

    def clean_string(self, text):
        text = "".join([word for word in text if word not in string.punctuation])
        text.lower()
        return text

    def combine_meta_products(self, first_meta_product, second_meta_product):
        first_product = first_meta_product.product
        second_product = second_meta_product.product

        if first_product and second_product:
            product = first_product
            product.meta_products = product.meta_products + second_product.meta_products
            second_product.delete()

        elif first_product:
            product = first_product
            product.meta_products.add(second_meta_product)

        elif second_product:
            product = second_product
            product.meta_products.add(first_meta_product)

        else:
            product = Product.objects.create()
            product.meta_products = [first_meta_product, second_meta_product]

        product.save()
        return product
