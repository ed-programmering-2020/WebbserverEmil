from django.db import models
import re, uuid, json


def get_file_path(instance, filename):
    return "%s.%s" % (uuid.uuid4(), "jpg")


class Product(models.Model):
    name = models.CharField('name', max_length=128)
    url = models.CharField('url', max_length=128, blank=True)
    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
    host = models.ForeignKey("products.website", related_name="meta_products", on_delete=models.CASCADE, null=True)
    _specs = models.CharField("specifications", max_length=4096, default=json.dumps([]))
    category_product = models.ForeignKey("products.BaseCategoryProduct",
                                         related_name="products",
                                         on_delete=models.CASCADE)

    def update(self, data):
        price_obj = Price(meta_product=self)
        price_obj.price = data.get("price")
        price_obj.save()

        specs = data.get("specs")
        if specs:
            specs_str = json.dumps(specs)
            while len(specs_str) > 4096:
                specs = specs[:-1]
                specs_str = json.dumps(specs)

            self._specs = specs_str
        self.save()

    def get_price(self):
        price = self.price_history.first()
        return price.price

    def get_specs(self):
        return json.loads(self._specs)


class Price(models.Model):
    product = models.ForeignKey(Product, related_name="price_history", on_delete=models.CASCADE)
    _price = models.PositiveIntegerField()
    date_seen = models.DateTimeField(auto_now_add=True)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        dot_pos = price.find(".")
        comma_pos = price.find(",")

        if 0 <= dot_pos < comma_pos:
            price = price[dot_pos:comma_pos]
        elif 0 <= comma_pos < dot_pos:
            price = price[comma_pos:dot_pos]

        if price != "" and price != None:
            price = int(re.sub("\D", "", str(price)))
            self._price = None if price >= 1000000 else price
        else:
            self._price = None

    def __str__(self):
        return "<Price {self.price} {self.date_seen}>".format(self=self)
