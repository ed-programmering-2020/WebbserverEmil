from django.db import models
from django.utils.safestring import mark_safe


class MetaProduct(models.Model):
    name = models.CharField('name', max_length=128)
    manufacturing_name = models.CharField("manufacturing_name", null=True, max_length=128)

    availability = models.PositiveSmallIntegerField(null=True)
    standard_price = models.PositiveIntegerField(null=True)
    campaign_price = models.PositiveIntegerField(null=True, blank=True)
    shipping = models.PositiveSmallIntegerField(null=True)
    used = models.BooleanField(default=False)

    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    review_count = models.PositiveSmallIntegerField(null=True)

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
        return (self.active_price is not None
                and self.is_active is True
                and self.availability > 0
                and self.used is False)

    def update(self, data, exclude=[]):
        # General update
        for key, value in data.items():
            if key not in exclude and hasattr(self, key):
                setattr(self, key, value)

        # Update price information
        price, campaign = data["price"], data["campaign"]
        if campaign is True:
            self.campaign_price = price
        else:
            self.standard_price = price
            self.campaign_price = None

    def url_tag(self):
        return mark_safe('<a href="%s" target="_blank">go to</a>' % self.url)
    url_tag.short_description = 'url'
    url_tag.allow_tags = True

    def __str__(self):
        return "<Product {self.name} {self.host.name}>".format(self=self)
