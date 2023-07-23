from django.urls import path
from . import views

urlpatterns = [
    path('', views.sayHello),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
]
