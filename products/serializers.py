from .models import BaseProduct, BaseSpecification, MetaProduct, Image, Website
from rest_framework import serializers


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ["id", "name", "short_url", "url", "description"]


class MetaProductSerializer(serializers.ModelSerializer):
    host = WebsiteSerializer(read_only=True)

    class Meta:
        model = MetaProduct
        fields = ["url", "host", "standard_price", "campaign_price"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "url", "host"]


class SpecificationSerializer(serializers.ModelSerializer):
    name = serializers.Field()
    value = serializers.Field()

    class Meta:
        model = BaseSpecification
        fields = ["name", "value"]


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    meta_products = MetaProductSerializer(many=True, read_only=True)
    specfications = SpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = BaseProduct
        fields = ["id", "slug", "name", "active_price", "images", "meta_products", "specifications", "disclaimer"]

    def get_images(self, instance):
        images = instance.images.all().order_by("placement")
        return ImageSerializer(images, many=True).data
