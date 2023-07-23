from django.urls import path
from . import views

urlpatterns = [
    path('', views.sayHello),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('get-csv/', views.get_csv, name='get_csv'),
    path('transform-csv/', views.transform_csv_field, name='transform_csv'), 
]
