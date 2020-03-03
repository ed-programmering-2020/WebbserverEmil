from rest_framework import serializers
from .models import BaseCategoryProduct, Website


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseCategoryProduct
        fields = ['id', 'name', 'price', 'get_websites', 'get_image']


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ["id", "name", "url", "description"]
