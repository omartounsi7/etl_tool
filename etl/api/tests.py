from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import CsvData

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import get_csv
from .models import CsvData
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import transform_csv_field
from .models import CsvData

class TransformCsvFieldViewTestCase(TestCase):
    def setUp(self):
        # Create a CsvData object for testing
        CsvData.objects.create(csv_data="Transaction ID,Transaction Date,Amount,Merchant Name\r\n123456,2022-04-01,50.00,Acme Retail\r\n")

    def test_transform_csv_field_with_valid_data(self):
        # Prepare the data for the POST request
        data = {
            'row': '2',
            'col': '3',
            'number': '25.00',
            'op': 'add',
        }

        # Make a POST request to the view
        factory = APIRequestFactory()
        request = factory.post('/api/transform-csv/', data)
        response = transform_csv_field(request)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the CSV data was updated correctly
        expected_csv_data = "Transaction ID,Transaction Date,Amount,Merchant Name\r\n123456,2022-04-01,75.00,Acme Retail\r\n"
        self.assertEqual(response.data['csv_data'], expected_csv_data)

    def test_transform_csv_field_with_invalid_coordinates(self):
        # Prepare invalid coordinates in the data for the POST request
        data = {
            'row': '5',
            'col': '3',
            'number': '25.00',
            'op': 'add',
        }

        # Make a POST request to the view
        factory = APIRequestFactory()
        request = factory.post('/api/transform-csv/', data)
        response = transform_csv_field(request)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check the error message in the response
        self.assertIn('Invalid coordinates.', response.data['error'])

class GetCsvViewTestCase(TestCase):
    def setUp(self):
        # Create some CsvData objects for testing
        CsvData.objects.create(csv_data="1,2,3\r\n4,5,6\r\n")
        CsvData.objects.create(csv_data="A,B,C\r\nD,E,F\r\n")

    def test_get_csv_with_data(self):
        # Make a GET request to the view
        factory = APIRequestFactory()
        request = factory.get('/api/get-csv/')
        response = get_csv(request)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data contains the last CsvData object's csv_data
        last_csv_data = CsvData.objects.last()
        expected_data = {'csv_data': last_csv_data.csv_data}
        self.assertEqual(response.data, expected_data)

    def test_get_csv_without_data(self):
        # Delete all CsvData objects to simulate no data
        CsvData.objects.all().delete()

        # Make a GET request to the view
        factory = APIRequestFactory()
        request = factory.get('/api/get-csv/')
        response = get_csv(request)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data is an empty dictionary
        self.assertEqual(response.data, {})

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
