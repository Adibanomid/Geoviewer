from django.db import models

class GeoTIFF(models.Model):
    file = models.FileField(upload_to='geotiffs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
