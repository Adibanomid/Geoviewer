from django.urls import path
from . import views
from .views import GeoTIFFUploadView

urlpatterns = [
    path('upload/', GeoTIFFUploadView.as_view(), name='upload_geotiff'),
    path('tiles/<str:filename>/<int:z>/<int:x>/<int:y>.png', views.tile_view, name='tile_view'),
    path('files/', views.list_geotiff_files, name='list_geotiff_files'),
]
