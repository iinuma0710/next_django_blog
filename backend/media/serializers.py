from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('title', 'thumbnail_url', 'display_url', 'original_url', 'uploaded_at')