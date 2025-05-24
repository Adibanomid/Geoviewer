from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import GeoTIFF
from .serializers import GeoTIFFSerializer
from django.core.files.uploadedfile import UploadedFile
from rio_tiler.io import Reader
from rio_tiler.colormap import cmap
from rio_tiler.utils import render
from rasterio.warp import transform_bounds
from rasterio.crs import CRS
from django.http import HttpResponse, Http404
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
import os
import mercantile

RASTER_DIR = os.path.join(settings.MEDIA_ROOT, 'geotiffs')

@permission_classes([IsAuthenticated])
class GeoTIFFUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        uploaded_file: UploadedFile = request.FILES.get('file')

        if not uploaded_file:
            return Response({"error": "No file provided."}, status=400)

        # File extension check
        if not uploaded_file.name.lower().endswith(('.tif', '.tiff')):
            return Response({"error": "Only .tif or .tiff files are allowed2."}, status=400)

        # MIME type check
        if uploaded_file.content_type not in ['image/tiff', 'image/x-tiff']:
            return Response({"error": "Invalid MIME type for TIFF."}, status=400)

        # Size limit check (500MB)
        if uploaded_file.size > 500 * 1024 * 1024:
            return Response({"error": "File size exceeds 500MB limit."}, status=400)

        # Proceed with saving if valid
        serializer = GeoTIFFSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'File uploaded successfully.'})
        return Response(serializer.errors, status=400)
    

def intersects(b1, b2):
    """
    Check if two bounding boxes intersect.
    b1 and b2 are (west, south, east, north)
    """
    return not (b2[0] > b1[2] or b2[2] < b1[0] or b2[1] > b1[3] or b2[3] < b1[1])

def tile_view(request, filename, z, x, y):
    tile = mercantile.Tile(x=int(x), y=int(y), z=int(z))
    tif_path = os.path.join(settings.MEDIA_ROOT, 'geotiffs', filename)
    if not os.path.exists(tif_path):
        return HttpResponse("File not found.", status=404)

    try:
        with Reader(tif_path) as src:

            # Check if the dataset has a CRS
            # if not src.dataset.crs:
            #     return HttpResponse("CRS is invalid or missing from this file.", status=400)
            
            # If CRS is None, set it dynamically (in-memory, no file overwrite)
            if src.dataset.crs is None:
                print(f"Assigning default CRS to {filename}")
                src.dataset.crs = CRS.from_epsg(4326)  # WGS84

            # Get bounds of the dataset in WGS84
            bounds = transform_bounds(src.dataset.crs, "EPSG:4326", *src.dataset.bounds)

            # Get bounds of the tile
            tile_bounds = mercantile.bounds(tile)

            # Check if tile intersects raster bounds
            if not intersects(bounds, tile_bounds):
                return HttpResponse("Tile outside raster bounds.", status=204)
            
            data, mask = src.tile(tile.x, tile.y, tile.z)

            # print(data[0].min(), data[0].max())
            img = render(
                data,
                mask=mask,
                colormap=cmap.get("plasma")
            )
        return HttpResponse(img, content_type="image/png")

    except Exception as e:
        print(f"Tile error for {filename} @ Z:{z} X:{x} Y:{y} — {str(e)}")
        return HttpResponse(f"Error rendering tile: {str(e)}", status=500)

@permission_classes([IsAuthenticated])
def list_geotiff_files(request):
    geotiff_dir = os.path.join(settings.MEDIA_ROOT, 'geotiffs')
    try:
        files = [
            f for f in os.listdir(geotiff_dir)
            if f.lower().endswith('.tif') or f.lower().endswith('.tiff')
        ]
    except FileNotFoundError:
        files = []

    return JsonResponse({"files": files})