from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CsvData
from .views import get_csv


class DownloadCsvTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.csv_data = "test_csv_data"
        self.file_name = "test_file.csv"
        self.csv_data_obj = CsvData.objects.create(csv_data=self.csv_data, file_name=self.file_name)

    def test_download_csv_success(self):
        client = APIClient()
        url = f'/api/download-csv/?file_name={self.file_name}'

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="{self.file_name}"')
        self.assertEqual(response.content.decode(), '"' + self.csv_data + '"')

    def test_download_csv_no_file_name(self):
        client = APIClient()
        url = '/api/download-csv/'

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "File name was not provided."})

    def test_download_csv_file_not_found(self):
        client = APIClient()
        invalid_file_name = "invalid_file.csv"
        url = f'/api/download-csv/?file_name={invalid_file_name}'

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "CSV data does not exist."})


class TransformCSVFieldTest(APITestCase):
    def setUp(self):
        # Create some CsvData objects for testing
        CsvData.objects.create(csv_data="1,2,3\r\n4,5,6\r\n7,8,9\r\nA,B,C\r\nD,E,F\r\n")

    def test_transform_single_field(self):
        # Define the data for the POST request
        data = {
            'startRow': '1',
            'startCol': '1',
            'number': '10',
            'op': 'add',
        }

        # Make the POST request to the view
        url = reverse('transform_csv')  # Adjust the URL name to match your actual URL configuration
        response = self.client.post(url, data)

        # Assert that the response has a 200 status code
        self.assertEqual(response.status_code, 200)

        # Get the updated CSV data from the response
        updated_csv_data = response.data.get('csv_data')

        # Assert that the updated CSV data contains the expected values
        expected_csv_data = "11.0,2,3\r\n4,5,6\r\n7,8,9\r\nA,B,C\r\nD,E,F"
        self.assertEqual(updated_csv_data, expected_csv_data)

    def test_transform_multiple_fields(self):
        # Define the data for the POST request
        data = {
            'startRow': '1',
            'startCol': '1',
            'endRow': '3',
            'endCol': '3',
            'number': '10',
            'op': 'add',
        }

        # Make the POST request to the view
        url = reverse('transform_csv')  # Adjust the URL name to match your actual URL configuration
        response = self.client.post(url, data)

        # Assert that the response has a 200 status code
        self.assertEqual(response.status_code, 200)

        # Get the updated CSV data from the response
        updated_csv_data = response.data.get('csv_data')

        # Assert that the updated CSV data contains the expected values
        expected_csv_data = "11.0,12.0,13.0\r\n14.0,15.0,16.0\r\n17.0,18.0,19.0\r\nA,B,C\r\nD,E,F"
        self.assertEqual(updated_csv_data, expected_csv_data)

    def test_invalid_inputs(self):
        # Define the data for the POST request
        data = {
            'startRow': '1',
            'startCol': '1',
            'endRow': '4',
            'endCol': '4',
            'number': '10',
            'op': 'add',
        }

        # Make the POST request to the view
        url = reverse('transform_csv')  # Adjust the URL name to match your actual URL configuration
        response = self.client.post(url, data)

        # Assert that the response has a 200 status code
        self.assertEqual(response.status_code, 400)

        # Get the updated CSV data from the response
        updated_csv_data = response.data.get('csv_data')

        # Assert that the updated CSV data contains the expected values
        expected_csv_data = None
        self.assertEqual(updated_csv_data, expected_csv_data)

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
