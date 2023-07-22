from django.urls import path
from . import views

urlpatterns = [
    path('', views.sayHello),
    path('upload/', views.upload_csv, name='upload_csv'),
]
