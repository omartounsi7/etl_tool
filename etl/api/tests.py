from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import CsvData

class CsvDataUploadViewTestCase(TestCase):
    def test_upload_csv_file(self):
        # Prepare a CSV file for the test
        csv_content = "Name, Age\nJohn, 30\nJane, 28\n"
        csv_file = SimpleUploadedFile("test.csv", csv_content.encode("utf-8"), content_type="text/csv")

        # Send a POST request to the view with the CSV file
        url = reverse('upload_csv')
        client = APIClient()
        response = client.post(url, {'csv_file': csv_file}, format='multipart')

        # Assert the response status code and data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the uploaded CSV data is stored in the database
        self.assertEqual(CsvData.objects.count(), 1)
        csv_data_obj = CsvData.objects.first()
        self.assertEqual(csv_data_obj.csv_data, csv_content)

    def test_upload_invalid_file_format(self):
        # Prepare a non-CSV file for the test
        invalid_file = SimpleUploadedFile("invalid_file.txt", b"some content", content_type="text/plain")

        # Send a POST request to the view with the invalid file
        url = reverse('upload_csv')
        client = APIClient()
        response = client.post(url, {'csv_file': invalid_file}, format='multipart')

        # Assert the response status code and error message
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid file format", response.data['error'])
