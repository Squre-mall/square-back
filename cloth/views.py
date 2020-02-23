from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from .models import Cloth
from .serializers import ClothSerializer

class ListCloth(generics.ListCreateAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer

class DetailCloth(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer