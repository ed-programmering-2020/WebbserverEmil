"""
from models import BaseProduct, MetaProduct, Image, Website
from rest_framework import serializers


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ["id", "name", "short_url", "url"]


class MetaProductSerializer(serializers.ModelSerializer):
    host = WebsiteSerializer(read_only=True)

    class Meta:
        model = MetaProduct
        fields = ["url", "host", "standard_price", "campaign_price", "shipping", "availability"]


class ImageSerializer(serializers.ModelSerializer):
    host = WebsiteSerializer(read_only=True)

    class Meta:
        model = Image
        fields = ["id", "url", "host"]


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    meta_products = serializers.SerializerMethodField()

    class Meta:
        model = BaseProduct
        fields = ["id", "slug", "name", "rating", "active_price", "images", "meta_products", "disclaimer"]

    def get_images(self, instance):
        images = instance.images.filter(is_active=True).order_by("placement")
        return ImageSerializer(images, many=True).data

    def get_meta_products(self, instance):
        serialized_meta_products = [MetaProductSerializer(meta_product).data
                                    for meta_product in instance.meta_products.all()
                                    if meta_product.is_servable is True]
        return serialized_meta_products
"""
