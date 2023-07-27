from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('upload/', index),
    path('upload-success/', index),
    path('list-files/', index) 
]