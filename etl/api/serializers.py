from rest_framework import serializers
from .models import CsvData

class CsvDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvData
        fields = ('id', 'csv_data', 'file_name', 'uploaded_at')
