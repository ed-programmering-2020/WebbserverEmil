from django.db import models
import re, uuid, json


def get_file_path(instance, filename):
    return "%s.%s" % (uuid.uuid4(), "jpg")


class Product(models.Model):
    name = models.CharField('name', max_length=128)
    url = models.CharField('url', max_length=128, blank=True)
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    host = models.ForeignKey("products.website", related_name="meta_products", on_delete=models.CASCADE, null=True)
    _specifications = models.CharField("specifications", max_length=4096, default=json.dumps([]))
    category_product = models.ForeignKey(
        "products.BaseCategoryProduct",
        related_name="products",
        on_delete=models.CASCADE
    )

    @property
    def price(self):
        price = self.price_history.first()
        return price.value

    @price.setter
    def price(self, price):
        price_instance = Price(meta_product=self)
        price_instance.value = price
        price_instance.save()

    @property
    def specifications(self):
        return json.loads(self._specifications)

    @specifications.setter
    def specifications(self, specifications):
        to_string = json.dumps(specifications)
        while len(to_string) > 4096:
            specifications = specifications[:-1]
            to_string = json.dumps(specifications)

        self._specifications = to_string

    def __str__(self):
        return "<Product {self.name} {self.host.name}>".format(self=self)


class Price(models.Model):
    product = models.ForeignKey(Product, related_name="price_history", on_delete=models.CASCADE)
    _value = models.PositiveIntegerField()
    date_seen = models.DateTimeField(auto_now_add=True)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, price):
        dot_pos = price.find(".")
        comma_pos = price.find(",")

        if 0 <= dot_pos < comma_pos:
            price = price[dot_pos:comma_pos]
        elif 0 <= comma_pos < dot_pos:
            price = price[comma_pos:dot_pos]

        if price != "" and price != None:
            price = int(re.sub("\D", "", str(price)))
            self._value = None if price >= 1000000 else price
        else:
            self._value = None

    def __str__(self):
        return "<Price {self.price} {self.date_seen}>".format(self=self)
