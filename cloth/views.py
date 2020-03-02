from django.shortcuts import render

# Create your views here.
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.http import Http404

from .models import Cloth
from .serializers import ClothSerializer

from django_filters.rest_framework import DjangoFilterBackend

class ListCloth(generics.ListCreateAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ClothSerializer.Meta.fields
    search_fields = ClothSerializer.Meta.fields
    ordering_fields = ClothSerializer.Meta.fields

class DetailCloth(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer

