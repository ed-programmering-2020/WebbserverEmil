from rest_framework import serializers
from .models import BaseCategoryProduct, Website


class CategoryProductSerializer(serializers.ModelSerializer):
    websites = serializers.ReadOnlyField()
    images = serializers.ReadOnlyField()
    specifications = serializers.ReadOnlyField()

    class Meta:
        model = BaseCategoryProduct
        fields = ["id", "slug", "active_price", "name", "websites", "images", "specifications"]


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ["id", "name", "url", "description"]
