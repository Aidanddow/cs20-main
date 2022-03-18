from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
import os


class StreamlineConfig(AppConfig):
    name = "streamline"

    def ready(self):
        autodiscover_modules("signals")

        from . import db_cleaning

        if os.environ.get("RUN_MAIN", None) != "true":
            db_cleaning.start_scheduler()


default_app_config = "streamline.apps.StreamlineConfig"
