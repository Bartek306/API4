from django.urls import path
from .views import archive_convert, convert

urlpatterns = [
    path('archive_convert', archive_convert),
    path('convert', convert)
]