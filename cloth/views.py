from django.shortcuts import render

# Create your views here.
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.http import Http404

from .models import Cloth
from .serializers import ClothSerializer

from django_filters.rest_framework import DjangoFilterBackend

cgDict = {
    'outer': 1,
    'top' : 2,
    'bottom':3,
}

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


class ListCategory(views.APIView):
    def get(self, request, category, format=None):
        queryset = Cloth.objects.filter(category=cgDict.get(category, ''))
        serializer = ClothSerializer(queryset, many=True)
        return Response(serializer.data)

class DetailCategory(views.APIView):
    def get_object(self, pk):
        try:
            return Cloth.objects.get(pk=pk)
        except Cloth.DoesNotExist:
            raise Http404

    def get(self, request, category, pk):
        cloth = self.get_object(pk)
        serializer = ClothSerializer(cloth)
        return Response(serializer.data)

    def put(self, request, category, pk, format=None):
        cloth = self.get_object(pk)
        serializer = ClothSerializer(cloth, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
