from django.db import models

class CsvData(models.Model):
    csv_data = models.TextField()
    file_name = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
