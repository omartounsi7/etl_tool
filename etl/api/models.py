from django.db import models

class CsvData(models.Model):
    csv_data = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
