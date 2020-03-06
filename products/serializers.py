from rest_framework import serializers
from .models import BaseCategoryProduct, Website


class CategoryProductSerializer(serializers.ModelSerializer):
    websites = serializers.SerializerMethodField("get_websites")
    images = serializers.SerializerMethodField("get_images")
    specifications = serializers.SerializerMethodField("get_specifications")

    class Meta:
        model = BaseCategoryProduct
        fields = ["id", "name", "websites", "images", "specifications"]


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ["id", "name", "url", "description"]
