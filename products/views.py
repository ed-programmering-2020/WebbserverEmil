from rest_framework.response import Response
from rest_framework import generics
from products.models import Category


class MatchAPI(generics.GenericAPIView):
    def get(self, request, name, *args, **kwargs):
        category = Category.objects.get(name=name)

        settings = {
            "usage": {
                "value": "gaming"
            },
            "price": {
                "range": (1000, 4000),
            },
            "size": {
                "values": (13.3, 15.6)
            },
            "priorities": {
                "battery": 5,
                "performance": 3,
                "storage": 7,
                "screen": 5,
            }
        }

        return Response(category.match(settings))
