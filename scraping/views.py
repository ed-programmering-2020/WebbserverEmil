from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import WebsiteSerializer
from .models import Website
from .combiner import Combiner

import json


class ProductsAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.data.get("products"))
        files = request.FILES

        Combiner(data, files)
        return Response({})
