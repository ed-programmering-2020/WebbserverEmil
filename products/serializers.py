from rest_framework import serializers
from .models import Product, Website


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', "get_image", "get_websites"]
