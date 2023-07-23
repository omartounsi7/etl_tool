from django.urls import path
from . import views

urlpatterns = [
    path('', views.sayHello),
    path('upload-csv/', views.CsvDataUploadView.as_view(), name='upload_csv')
]
