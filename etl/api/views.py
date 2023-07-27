from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import CsvData
from .serializers import CsvDataSerializer

from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
 
# Create your views here.
def sayHello(request):
    return HttpResponse("Hello World!") 

def validate_op(op, current_value, number):
    if op == "add":
        new_value =  current_value + float(number)
    elif op == "sub":
        new_value =  current_value - float(number)
    elif op == "mul":
        new_value =  current_value * float(number)
    elif op == "div":
        new_value =  current_value / float(number)
    else:
        print("Invalid op!")
        raise ValueError("Invalid operation.")
    return new_value

def update_field_value(csv_data, row, col, op, number):
    # Get the field value
    rows = csv_data.strip().split('\r\n')
    if row < 1 or row > len(rows):
        raise ValueError("Invalid coordinates.")
    
    columns = rows[row - 1].split(',')
    if col < 1 or col > len(columns):
        raise ValueError("Invalid coordinates.")
    
    field_val = columns[col - 1]
    field_val = field_val.replace('.', '', 1).replace('e', '', 1).replace('-', '', 1).replace('$', '', 1).replace('%', '', 1).replace('€', '', 1).replace('£', '', 1)
    
    # Validate the field value
    if not field_val.isnumeric():
        print("Not numeric")
        raise ValueError("The field at the given coordinates does not contain a number.")

    # Perform the operation
    current_value = float(columns[col - 1].replace('$', '', 1).replace('%', '', 1).replace('€', '', 1).replace('£', '', 1))
    new_value = validate_op(op, current_value, number)
    columns[col - 1] = str(new_value)
    rows[row - 1] = ','.join(columns)
    csv_data = '\r\n'.join(rows)

    return csv_data

@api_view(['POST'])
def transform_csv_field(request):
    if request.method == 'POST':
        # Get the coordinates and number from the request
        start_row_str = request.data.get('startRow', None)
        start_col_str = request.data.get('startCol', None)
        end_row_str = request.data.get('endRow', None)
        end_col_str = request.data.get('endCol', None)
        number_str = request.data.get('number', None) 
        op = request.data.get('op', None)

        # Check if all the required parameters are present
        if start_row_str is None or start_col_str is None or number_str is None or op is None:
            print("Missing params.")
            raise ValueError("Missing parameters. Please provide start row, start column, operation and number.")

        try:
            start_row = int(start_row_str) 
            start_col = int(start_col_str)
            number = float(number_str)

            # Fetch the latest CSV data
            csv_data_obj = CsvData.objects.last()
            if not csv_data_obj:
                print("No CSV data found")
                return Response({"error": "No CSV data found."}, status=status.HTTP_404_NOT_FOUND)

            csv_data = csv_data_obj.csv_data

            # Check if user inputted end coordinates
            if (not end_row_str or not end_col_str):
                # Update one field only 
                csv_data = update_field_value(csv_data, start_row, start_col, op, number)
            else:
                end_row = int(end_row_str) 
                end_col = int(end_col_str)

                # Determine which one of the two inputted fields (start and end) is the uppermost in the table
                if(start_row <= end_row):
                    first_row = start_row
                    last_row = end_row
                    if(start_col <= end_col):
                        first_col = start_col
                        last_col = end_col
                    else:
                        first_col = end_col
                        last_col = start_col
                else:
                    first_row = end_row
                    last_row = start_row
                    if(start_col <= end_col):
                        first_col = start_col
                        last_col = end_col
                    else:
                        first_col = end_col
                        last_col = start_col

                # Update every field between the first and the last field
                for x in range(first_row, last_row + 1):
                    for y in range(first_col, last_col + 1):
                        csv_data = update_field_value(csv_data, x, y, op, number)

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
    file_name = request.GET.get('file_name', None)

    if not file_name:
        return Response({"error": "File name was not provided."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        csv_data_obj = CsvData.objects.get(file_name=file_name)
    except CsvData.DoesNotExist:
        return Response({"error": "File does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    data = {'csv_data': csv_data_obj.csv_data} if csv_data_obj else {}
    
    return Response(data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_csv(request):
    file_name = request.GET.get('file_name', None)

    if not file_name:
        return Response({"error": "File name was not provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        csv_data_obj = CsvData.objects.get(file_name=file_name)
    except CsvData.DoesNotExist:
        return Response({"error": "File does not exist."}, status=status.HTTP_404_NOT_FOUND)

    csv_data_obj.delete_file()
    return Response({"message": f"CSV file '{file_name}' deleted successfully."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_files(request):
    # Retrieve all CsvData objects from the database
    csv_data_objects = CsvData.objects.all()

    # Serialize the objects
    serializer = CsvDataSerializer(csv_data_objects, many=True)

    # Return the serialized data as the response
    return Response(serializer.data)

@api_view(['GET'])
def download_csv(request):
    file_name = request.GET.get('file_name', None)

    if not file_name:
        return Response({"error": "File name was not provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        csv_data = CsvData.objects.get(file_name=file_name)
    except CsvData.DoesNotExist:
        return Response({"error": "File does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    response = Response(csv_data.csv_data, content_type='text/csv', status=status.HTTP_200_OK)
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    response['X-Accel-Redirect'] = f'/media/{file_name}'

    return response

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
        
        # Check if a file with the same name already exists
        if CsvData.objects.filter(file_name=csv_file.name).exists():
            return Response({"error": "A file with the same name already exists. Please choose a different name."}, status=status.HTTP_409_CONFLICT)

        try:
            # Read the contents of the CSV file
            csv_data = csv_file.read().decode('utf-8')
            
            # Save the CSV data to the database along with the file name
            csv_data_obj = CsvData(csv_data=csv_data, file_name=csv_file.name)
            csv_data_obj.save()


            # Use FileSystemStorage to save the CSV file in the media folder
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            fs.save(csv_file.name, csv_file)

            # Serialize the saved object and return the response
            serializer = CsvDataSerializer(csv_data_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
