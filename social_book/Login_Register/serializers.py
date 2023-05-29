from rest_framework import serializers
from .models import UploadedFiles


class UploadedFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFiles
        fields = ['id', 'title', 'description', 'visibility', 'cost', 'year_published', 'file']
