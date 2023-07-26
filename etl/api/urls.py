from django.urls import path
from . import views

urlpatterns = [
    path('', views.sayHello),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('delete-csv/', views.delete_csv, name='delete_csv'),
    path('list-files/', views.list_files, name='list_files'),
    path('get-csv/', views.get_csv, name='get_csv'),
    path('transform-csv/', views.transform_csv_field, name='transform_csv'), 
]
