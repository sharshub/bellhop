from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import autodiscover_modules


class BellHopConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bellhop"

    def ready(self):
        super().ready()
        autodiscover_modules("uploaders")

        if not hasattr(settings, "BELLHOP"):
            raise ImproperlyConfigured("BellHop not configured correctly")

        from bellhop import bellhop

        bellhop.register_engine(**settings.BELLHOP)
