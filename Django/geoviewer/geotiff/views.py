from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import GeoTIFF
from .serializers import GeoTIFFSerializer

from rio_tiler.io import Reader
from rio_tiler.colormap import cmap  # Updated import
from rio_tiler.utils import render
from django.http import HttpResponse, Http404
from django.conf import settings
import os
# from starlette.responses import Response  # Or use Django's HttpResponse with correct content-type
import mercantile


class GeoTIFFUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = GeoTIFFSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'File uploaded successfully.'})
        return Response(serializer.errors, status=400)


# Update this path to point to your raster storage directory
RASTER_DIR = os.path.join(settings.MEDIA_ROOT, 'geotiffs')

import os
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from rio_tiler.io import Reader
from rio_tiler.colormap import cmap
import mercantile

from .serializers import GeoTIFFSerializer


class GeoTIFFUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        uploaded_file: UploadedFile = request.FILES.get('file')

        if not uploaded_file:
            return Response({"error": "No file provided."}, status=400)

        # ✅ File extension check
        if not uploaded_file.name.lower().endswith(('.tif', '.tiff')):
            return Response({"error": "Only .tif or .tiff files are allowed2."}, status=400)

        # ✅ MIME type check (very basic but useful)
        if uploaded_file.content_type not in ['image/tiff', 'image/x-tiff']:
            return Response({"error": "Invalid MIME type for TIFF."}, status=400)

        # ✅ Size limit check (500MB)
        if uploaded_file.size > 500 * 1024 * 1024:
            return Response({"error": "File size exceeds 500MB limit."}, status=400)

        # ✅ Proceed with saving if valid
        serializer = GeoTIFFSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'File uploaded successfully.'})
        return Response(serializer.errors, status=400)



# Update this path to point to your raster storage directory
RASTER_DIR = os.path.join(settings.MEDIA_ROOT, 'geotiffs')

def tile_view(request, filename, z, x, y):
    tile = mercantile.Tile(x=int(x), y=int(y), z=int(z))
    tif_path = os.path.join(settings.MEDIA_ROOT, 'geotiffs', filename)

    if not os.path.exists(tif_path):
        return HttpResponse("File not found.", status=404)

    try:
        with Reader(tif_path) as src:
            data, mask = src.tile(tile.x, tile.y, tile.z)
            # print(data[0].min(), data[0].max())
            img = render(
                data,
                mask=mask,
                colormap=cmap.get("plasma")
            )
        return HttpResponse(img, content_type="image/png")

    except Exception as e:
        return HttpResponse(f"Error rendering tile: {str(e)}", status=500)
