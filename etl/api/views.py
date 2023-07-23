from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import CsvData
from .serializers import CsvDataSerializer

from django.http import HttpResponse

# Create your views here.
def sayHello(request):
    return HttpResponse("Hello World!")

@api_view(['POST'])
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file', None)

        # Check if a file was uploaded
        if not csv_file:
            return Response({"error": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the uploaded file is a CSV file
        if not csv_file.name.lower().endswith('.csv'):
            return Response({"error": "Invalid file format. Please upload a CSV file."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the contents of the CSV file
            csv_data = csv_file.read().decode('utf-8')
            
            # Save the CSV data to the database
            csv_data_obj = CsvData(csv_data=csv_data)
            csv_data_obj.save()

            # Serialize the saved object and return the response
            serializer = CsvDataSerializer(csv_data_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
