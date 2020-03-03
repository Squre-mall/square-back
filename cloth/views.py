from django.shortcuts import render

# Create your views here.
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.http import Http404

from .models import *
from .serializers import *

from django_filters.rest_framework import DjangoFilterBackend
import django_filters

class ListCloth(generics.ListCreateAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [a for a in ClothSerializer.Meta.fields if a != 'price']
    search_fields = [a for a in ClothSerializer.Meta.fields if a != 'price']
    ordering_fields = [a for a in ClothSerializer.Meta.fields if a != 'price']

class DetailCloth(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer

class ListClothDetailMusinsa(generics.ListCreateAPIView):
    queryset = Cloth_Detail_Musinsa.objects.all()
    serializer_class = ClothDetailMusinsaSerializer
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [a for a in ClothDetailMusinsaSerializer.Meta.fields]
    search_fields = [a for a in ClothDetailMusinsaSerializer.Meta.fields]
    ordering_fields = [a for a in ClothDetailMusinsaSerializer.Meta.fields]

class DetailClothDetailMusinsa(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cloth_Detail_Musinsa.objects.all()
    serializer_class = ClothDetailMusinsaSerializer