from rest_framework import serializers
from .models import GeoTIFF

class GeoTIFFSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoTIFF
        fields = '__all__'