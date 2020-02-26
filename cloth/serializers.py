from rest_framework import serializers
from .models import *

class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Cloth