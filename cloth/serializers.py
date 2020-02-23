from rest_framework import serializers
from .models import Cloth

class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        # fields = (
        #     'id',
        #     'brand',
        #     'title',
        #     'date',
        #     'clothImg',
        #     'price',
        #     'category',
        # )
        model = Cloth