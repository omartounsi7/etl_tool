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

def get_field_value(csv_data, row, col):
    rows = csv_data.strip().split('\r\n')
    if row < 1 or row >= len(rows) or col < 1:
        raise ValueError("Invalid coordinates.")
    
    columns = rows[row - 1].split(',')
    if col >= len(columns):
        raise ValueError("Invalid coordinates.")
    
    return columns[col - 1]

@api_view(['POST'])
def transform_csv_field(request):
    if request.method == 'POST':
        # Get the coordinates and number from the request
        row_str = request.data.get('row', None)
        col_str = request.data.get('col', None)
        number_str = request.data.get('number', None)
        op = request.data.get('op', None)

        # Check if all the required parameters are present
        if row_str is None or col_str is None or number_str is None or op is None:
            print("Missing params.")
            return Response({"error": "Missing parameters. Please provide row, col, op and number."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            row = int(row_str) 
            col = int(col_str)
            number = float(number_str) 

            # Fetch the latest CSV data
            csv_data_obj = CsvData.objects.last()
            if not csv_data_obj:
                print("No CSV data found.")
                return Response({"error": "No CSV data found."}, status=status.HTTP_404_NOT_FOUND)

            csv_data = csv_data_obj.csv_data
            field_val = get_field_value(csv_data, row, col)
            
            field_val = field_val.replace('.', '', 1).replace('e', '', 1).replace('-', '', 1).replace('$', '', 1).replace('%', '', 1).replace('€', '', 1).replace('£', '', 1)
            # Validate the field at the given coordinates (A4) contains a number
            if not field_val.isnumeric():
                print("Not numeric")
                return Response({"error": "The field at the given coordinates does not contain a number."}, status=status.HTTP_400_BAD_REQUEST)

            # Perform the addition operation
            rows = csv_data.strip().split('\r\n')
            columns = rows[row - 1].split(',')
            current_value = float(columns[col - 1].replace('$', '', 1).replace('%', '', 1).replace('€', '', 1).replace('£', '', 1))

            if op == "add":
                new_value =  current_value + float(number)
            elif op == "sub":
                new_value =  current_value - float(number)
            elif op == "mul":
                new_value =  current_value * float(number)
            elif op == "div":
                new_value =  current_value / float(number)
            else:
                print("Invalid op")
                return Response({"error": "Invalid operation."}, status=status.HTTP_400_BAD_REQUEST)

            columns[col - 1] = str(new_value)
            rows[row - 1] = ','.join(columns)
            csv_data = '\r\n'.join(rows)

            # Save the updated CSV data
            csv_data_obj.csv_data = csv_data
            csv_data_obj.save()

            # Return the updated CSV data
            data = {'csv_data': csv_data}
            return Response(data, status=status.HTTP_200_OK)

        except ValueError as e:
            print("Value error!") 
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_csv(request):
    csv_data = CsvData.objects.last()
    data = {'csv_data': csv_data.csv_data} if csv_data else {}
    return Response(data)


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
