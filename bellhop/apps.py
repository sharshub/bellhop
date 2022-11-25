from django import apps

from bellhop.main import BellHop


class BellHopConfig(apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bellhop"

    def ready(self):
        all_models = apps.apps.get_models()

        for model in all_models:
            if hasattr(model, "mount_uploader"):
                BellHop.register(model)
