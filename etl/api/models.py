from django.conf import settings
from django.db import models
import os

class CsvData(models.Model):
    csv_data = models.TextField()
    file_name = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def delete_file(self):
        # Delete the file from the media folder
        file_path = os.path.join(settings.MEDIA_ROOT, self.file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete the CsvData object from the database
        self.delete()