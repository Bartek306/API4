from django.urls import path
from .views import string

urlpatterns = [
    path('string', string)
]