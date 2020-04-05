from django.db import models


class MetaProduct(models.Model):
    name = models.CharField('name', max_length=128)
    manufacturing_name = models.CharField("manufacturing_name", null=True, max_length=128)

    availability = models.PositiveSmallIntegerField()
    standard_price = models.PositiveIntegerField()
    campaign_price = models.PositiveIntegerField(null=True)
    shipping = models.PositiveSmallIntegerField()

    url = models.CharField('url', max_length=128)
    host = models.ForeignKey("products.website", related_name="meta_products", on_delete=models.CASCADE, null=True)

    is_active = models.BooleanField(default=True)
    product = models.ForeignKey(
        "products.BaseProduct",
        related_name="meta_products",
        null=True,
        on_delete=models.CASCADE
    )

    @property
    def active_price(self):
        if self.campaign_price is not None:
            return self.campaign_price
        else:
            return self.standard_price

    @property
    def effective_price(self):
        return self.active_price + self.shipping

    @property
    def is_servable(self):
        return self.active_price is not None and self.is_active is True and self.availability > 0

    def update_price(self, price, campaign):
        if campaign is True:
            self.campaign_price = price
        else:
            self.standard_price = price
            self.campaign_price = None

    def __str__(self):
        return "<Product {self.name} {self.host.name}>".format(self=self)