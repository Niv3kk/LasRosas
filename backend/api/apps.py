# backend/api/apps.py
from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    label = "api"

    def ready(self):
        # fuerza que se importe models al iniciar la app
        from . import models  # noqa
