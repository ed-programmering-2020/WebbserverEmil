from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import WebsiteSerializer
from .models import Website
from .combiner import Combiner

import json


class WebsitesAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = WebsiteSerializer

    def get(self, request, *args, **kwargs):
        website = Website.objects.filter(has_run=False).first()
        if not website:
            Website.objects.all().update(has_run=False)
            website = Website.objects.filter(has_run=False).first()

        website.has_run = True
        website.save()

        return Response({"website": WebsiteSerializer(website).data})


class ProductsAPI(generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.data.get("products"))
        files = request.FILES

        Combiner(data, files)
        return Response({})
