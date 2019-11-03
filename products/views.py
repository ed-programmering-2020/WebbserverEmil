from rest_framework.response import Response
from rest_framework import generics


class CategoriesAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):

        return Response({})


class ProductsAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):

        return Response({})
