from django.urls import path
from .views import GeoTIFFUploadView

urlpatterns = [
    path('upload/', GeoTIFFUploadView.as_view(), name='upload_geotiff'),
]
