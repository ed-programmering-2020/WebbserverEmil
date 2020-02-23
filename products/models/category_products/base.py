from ..polymorphism import PolymorphicModel
from ..specifications import AlternativeSpecificationName, SpecificationType
from difflib import SequenceMatcher
from collections import defaultdict
from django.db import models


class BaseCategoryProduct(PolymorphicModel):
    name = models.CharField('name', max_length=128)
    manufacturing_name = models.CharField("manufacturing name", max_length=128)
    score = models.DecimalField("score", max_digits=9, decimal_places=9, null=True)
    is_active = models.BooleanField(default=True)
    is_ranked = models.BooleanField("is ranked", default=False)

    def most_frequent(self, List):
        return max(set(List), key=List.count) if List != [] else None

    def update(self):
        # Gather meta data
        data = defaultdict(default_factory=[])
        for product in self.products.all():
            data["names"].append(product.name)
            data["specifications"].append(product.get_specs())
            data["manufacturing_names"].append(product.manufacturing_name)
            data["prices"].append(product.get_price())

        # Update product
        if len(data["prices"]) >= 2:
            if self.check_price_outlier(data["prices"]):
                data["prices"].remove(min(data["prices"]))

            self.price = min(data["prices"])

        if self.manufacturing_name is None:
            for manufacturing_name in data["manufacturing_names"]:
                if manufacturing_name:
                    self.manufacturing_name = manufacturing_name
                    break

        self.update_name(data["names"])
        self.update_specs(data["specs"])
        self.is_ranked = False
        self.save()

    def update_name(self, names):
        words = {}
        for name in names:
            split_words = name.split(" ")

            for other_name in names:
                if other_name != name:
                    other_split_words = other_name.split(" ")

                    for pos, word in enumerate(other_split_words):
                        for split_word in split_words:
                            if SequenceMatcher(None, split_word, word).ratio() >= 0.9 and pos >= 0:
                                if word in words:
                                    words[word].append(pos)
                                else:
                                    words[word] = [pos]

        words_copy = words.copy()
        removed_words = []
        for word in words_copy:
            if word not in removed_words:
                for other_word in words_copy:
                    if word != other_word:
                        if SequenceMatcher(None, other_word, word).ratio() >= 0.9:
                            length = len(words[word])
                            other_word = words.get(other_word, None)
                            if not other_word:
                                other_length = len(other_word)

                                if length >= other_length:
                                    words.pop(other_word, None)
                                    removed_words.append(other_word)
                                else:
                                    words.pop(word, None)
                                    removed_words.append(word)

        calc_words = {word: (sum(p) / len(p)) for (word, p) in words.items()}
        sorted_words = sorted(calc_words.items(), key=lambda kv: kv[1])
        name = ""
        for word, pos in sorted_words:
            if len(name) > 0:
                name += " " + word
            else:
                name = word

        if name == "" and names != []:
            name = names[0]

        self.name = name

    def update_specs(self, specs_list):
        updated_specs = []
        for specs in specs_list:
            for spec in specs:
                key = spec[0]
                value = spec[1]

                # Create/get spec key
                try:
                    alternative_specification_name = AlternativeSpecificationName.objects.get(name__iexact=key)

                    # Create/get if it belongs to spec group
                    specification_type = alternative_specification_name.specification_type
                    if specification_type:
                        specification_model = specification_type.get_specification_model()

                        value = spec_group.process_value(value)

                        try:
                            self.spec_values.get(value__iexact=value, spec_key=spec_key)
                        except SpecValue.DoesNotExist:
                            spec_value = SpecValue.objects.create(value=value, spec_key=spec_key)
                            spec_value.products.add(self)
                            spec_value.save()
                            updated_specs.append(spec_value)

                except AlternativeSpecificationName.DoesNotExist:
                    AlternativeSpecificationName.objects.create(name=key)

    def check_price_outlier(self, prices):
        sorted_prices = sorted(prices)
        relative_min_price = sorted_prices[1] / 2

        return sorted_prices[0] >= relative_min_price

    def get_websites(self):
        urls = []
        prices = []
        for meta_product in self.meta_products.all():
            urls.append(meta_product.url)
            prices.append(meta_product.get_price())

        if self.check_price_outlier(prices):
            i = prices.index(min(prices))
            urls.pop(i)
            prices.pop(i)

        return list(zip(urls, prices))

    def get_image(self):
        images = [mp.image for mp in self.meta_products.all() if mp.image]
        if len(images) > 0:
            return images[0].url
        return None


class CategoryAlternativeName(models.Model):
    name = models.CharField("name", max_length=32)
    category_product = models.ForeignKey(BaseCategoryProduct, related_name="alternative_names", on_delete=models.CASCADE)

