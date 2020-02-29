from rest_framework import serializers
from .models import *

class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id',) + tuple(a.name for a in Cloth._meta.get_fields())
        model = Cloth