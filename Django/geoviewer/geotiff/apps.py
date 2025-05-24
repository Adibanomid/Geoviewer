from django.apps import AppConfig


class GeotiffConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'geotiff'

# def create_test_user():
#     if not User.objects.filter(username='testuser').exists():
#         User.objects.create_user(username='testuser', password='testpass')