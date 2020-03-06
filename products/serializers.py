from rest_framework import serializers
from .models import BaseCategoryProduct, Website


class CategoryProductSerializer(serializers.ModelSerializer):
    websites = serializers.Field(source="websites")
    images = serializers.Field(source="images")
    specifications = serializers.Field(source="specifications")

    class Meta:
        model = BaseCategoryProduct
        fields = ['id', 'name']


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ["id", "name", "url", "description"]
