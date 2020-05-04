from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.db.models import Q
from django.db import models
import json


class Image(models.Model):
    url = models.CharField('url', max_length=256)
    host = models.ForeignKey("products.Website", on_delete=models.CASCADE)
    placement = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    product = models.ForeignKey("products.BaseProduct", on_delete=models.CASCADE, related_name="images")
    is_active = models.BooleanField(default=False)

    def thumbnail(self):
        return mark_safe('<img src="%s" height="50" />' % self.url)
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True


class Website(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('name', max_length=128)
    short_url = models.CharField("short url", max_length=64)
    url = models.CharField('url', max_length=256)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.short_url


class BaseProduct(models.Model):
    score_bias_table = None

    # Identification
    name = models.CharField('name', max_length=128, null=True)
    manufacturing_name = models.CharField("manufacturing name", max_length=128, unique=True, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    # Pricing
    effective_price = models.PositiveIntegerField(null=True)
    active_price = models.PositiveIntegerField(null=True)

    # Measurements
    height = models.PositiveSmallIntegerField(null=True, help_text="in millimeters")
    width = models.PositiveSmallIntegerField(null=True, help_text="in millimeters")
    depth = models.PositiveSmallIntegerField(null=True, help_text="in millimeters")
    weight = models.DecimalField(null=True, max_digits=3, decimal_places=2, help_text="in kilograms")

    # Other
    disclaimer = models.CharField("disclaimer", max_length=128, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    guarantee = models.PositiveSmallIntegerField(null=True, help_text="in years")

    @classmethod
    def match(cls, settings):
        model_instances = cls.objects.exclude(active_price=None).filter(is_active=True)
        price_range_dict = json.loads(settings["price"])
        model_instances = model_instances.filter(Q(effective_price__gte=price_range_dict["min"]),
                                                 Q(effective_price__lte=price_range_dict["max"]))
        return model_instances

    @staticmethod
    def get_relative_score(spec, baseline):
        if spec is None:
            return 0

        return float(spec) / baseline

    @staticmethod
    def get_type_score(spec, types):
        if spec is None:
            return 0

        spec = spec.lower()
        for i, spec_types in enumerate(types):
            for spec_type in spec_types:
                if spec_type in spec:
                    return i

        return 0

    @staticmethod
    def get_benchmarked_score(spec):
        if spec is None:
            return 0

        return float(spec.score)

    @classmethod
    def get_bias(cls, spec_name, usage, priorities=None, group=None):
        bias = cls.score_bias_table[spec_name][usage]

        if priorities is not None:
            identifier = spec_name if group is None else group
            bias += priorities[identifier]

        return bias

    def calculate_score(self, score, price_range):
        absolute_delta = price_range["max"] - price_range["min"]
        mid = absolute_delta * 0.5 + price_range["min"]
        delta_price = abs(self.active_price - mid)
        relative_distance = (1 - (delta_price / absolute_delta))**2

        score = score * relative_distance
        if self.rating is not None:
            rating = self.rating
        else:
            rating = 1
        return (score / self.active_price) * rating

    def save(self, *args, **kwargs):
        if self.name is not None:
            self.slug = slugify(self.name)
        super(BaseProduct, self).save(*args, **kwargs)

    def update(self, data, exclude=[]):
        # General update
        for key, value in data.items():
            if key not in exclude and hasattr(self, key):
                setattr(self, key, value)

        # Get price and ratings from meta product children
        prices, total_review_count, combined_ratings = [], 0, 0
        for meta_product in self.meta_products.all():
            if meta_product.is_servable is True:
                prices.append((meta_product.active_price, meta_product.effective_price))

            if meta_product.rating is not None and meta_product.review_count is not None:
                total_review_count += meta_product.review_count
                combined_ratings += meta_product.review_count * meta_product.rating

        # Update price
        if len(prices) > 0:
            sorted_prices = sorted(prices, key=lambda price_tuple: price_tuple[1])
            self.active_price, self.effective_price = sorted_prices[0]

        # Update rating
        if total_review_count > 0:
            self.rating = combined_ratings / total_review_count

    def __str__(self):
        return "<Product %s>" % self.name


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
    host = models.ForeignKey(Website, related_name="meta_products", on_delete=models.CASCADE, null=True)

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
