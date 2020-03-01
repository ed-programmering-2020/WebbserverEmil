from rest_framework import serializers
from .models import BaseCategoryProduct


class CategoryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseCategoryProduct
        fields = ['id', 'name', 'price', 'get_websites', 'get_image']
