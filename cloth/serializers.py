from rest_framework import serializers
from .models import *

class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id',) + tuple(a.name for a in Cloth._meta.get_fields())
        model = Cloth

class ClothDetailMusinsaSerializer(serializers.ModelSerializer):
    class Meta:
        fields = tuple(a.name for a in Cloth_Detail_Musinsa._meta.get_fields())
        model = Cloth_Detail_Musinsa