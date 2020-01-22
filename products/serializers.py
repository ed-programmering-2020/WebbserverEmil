from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Product
        fields = ('id', 'name', "image_url", "get_websites")

    def get_image_url(self, obj):
        return obj.get_image().url
