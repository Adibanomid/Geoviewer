from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import GeoTIFF
from .serializers import GeoTIFFSerializer

class GeoTIFFUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = GeoTIFFSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'File uploaded successfully.'})
        return Response(serializer.errors, status=400)

from rio_tiler.io import Reader
from rio_tiler.colormap import cmap  # Updated import
from rio_tiler.utils import render
from django.http import HttpResponse, Http404
from django.conf import settings
import os

# from starlette.responses import Response  # Or use Django's HttpResponse with correct content-type
import mercantile

# Update this path to point to your raster storage directory
RASTER_DIR = os.path.join(settings.MEDIA_ROOT, 'geotiffs')

def tile_view(request, filename, z, x, y):
    tile = mercantile.Tile(x=int(x), y=int(y), z=int(z))
    tif_path = os.path.join(settings.MEDIA_ROOT, 'geotiffs', filename)

    with Reader(tif_path) as src:
        data, mask = src.tile(tile.x, tile.y, tile.z)
        img = render(
            data,
            mask=mask,
            colormap=cmap.get("viridis")  # or "cfastie", "plasma", "inferno"
        )

    return HttpResponse(img, content_type="image/png")
