from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('upload/', index),
    path('display-file/', index),
    path('list-files/', index) 
]