from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.db.models import Q
from django.db import models

from products.models.specifications.base import DynamicSpecification
from decimal import Decimal

import json


class Image(models.Model):
    url = models.CharField('url', max_length=256)
    host = models.ForeignKey("products.Website", on_delete=models.CASCADE)
    placement = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(4)])
    product = models.ForeignKey("products.BaseProduct", on_delete=models.CASCADE, related_name="images")
    is_active = models.BooleanField(default=False)
    is_duplicate = models.BooleanField(default=False)

    def thumbnail(self):
        return mark_safe('<img src="%s" height="50" style="%s"/>'
                         % (self.url, "opacity: 0.5;" if self.is_duplicate else ""))
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True


class BaseProduct(models.Model):
    specification_info = None

    name = models.CharField('name', max_length=128, null=True)
    slug = models.SlugField(null=True, blank=True)
    manufacturing_name = models.CharField("manufacturing name", max_length=128, null=True, blank=True)

    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)

    effective_price = models.PositiveIntegerField(null=True)
    active_price = models.PositiveIntegerField(null=True)

    disclaimer = models.CharField("disclaimer", max_length=128, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    @classmethod
    def match(cls, settings):
        model_instances = cls.objects.exclude(active_price=None).filter(is_active=True)
        price_range_dict = json.loads(settings["price"])
        model_instances = model_instances.filter(Q(effective_price__gte=price_range_dict["min"]),
                                                 Q(effective_price__lte=price_range_dict["max"]))
        return model_instances

    def calculate_score(self, score, price_range):
        absolute_delta = price_range["max"] - price_range["min"]
        mid = absolute_delta * 0.5 + price_range["min"]
        delta_price = abs(self.active_price - mid)
        relative_distance = (1 - (delta_price / absolute_delta))**2

        score = score * Decimal(relative_distance)
        if self.rating is not None:
            rating = self.rating
        else:
            rating = 1
        return (score / self.active_price) * rating

    def save(self, *args, **kwargs):
        if self.name is not None:
            self.slug = slugify(self.name)
        super(BaseProduct, self).save(*args, **kwargs)

    def update_price(self):
        prices = [(meta_product.active_price, meta_product.effective_price)
                  for meta_product in self.meta_products.all() if meta_product.is_servable is True]
        if len(prices) > 0:
            sorted_prices = sorted(prices, key=lambda price_tuple: price_tuple[1])
            self.active_price, self.effective_price = sorted_prices[0]

    def update_specifications(self, specifications):
        for key, value in specifications.items():
            mod = __import__("products")
            for component in ["models", key]:
                mod = getattr(mod, component)

            attribute_name = mod.to_attribute_name()
            attribute = getattr(self, attribute_name)
            if attribute is None:
                value = mod.process_value(value)
                specification = mod.find_existing(value)

                if specification is None and issubclass(mod, DynamicSpecification):
                    specification = mod.objects.create(value=value)
                    specification.update_score()
                    specification.save()

                if specification is not None:
                    setattr(self, attribute_name, specification)

    def update_rating(self):
        total_review_count = 0
        combined_ratings = 0
        for meta_product in self.meta_products.all():
            if meta_product.rating is not None and meta_product.review_count is not None:
                total_review_count += meta_product.review_count
                combined_ratings += meta_product.review_count * meta_product.rating

        if total_review_count > 0:
            self.rating = combined_ratings / total_review_count

    def __str__(self):
        return "<Product %s>" % self.name
