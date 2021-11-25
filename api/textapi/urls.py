from django.urls import path
from .views import archive_convert

urlpatterns = [
    path('archive_convert', archive_convert)

]