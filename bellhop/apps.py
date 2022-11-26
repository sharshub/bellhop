from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class BellHopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bellhop"

    def ready(self):
        super().ready()
        autodiscover_modules("uploaders")
