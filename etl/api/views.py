from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CsvFileSerializer

from django.http import HttpResponse

# Create your views here.
def sayHello(request):
    return HttpResponse("Hello World!")

@api_view(['POST'])
def upload_csv(request):
    serializer = CsvFileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
