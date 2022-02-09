from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class StreamlineConfig(AppConfig):
    name = 'streamline'

    def ready(self):
        autodiscover_modules('signals')

default_app_config = 'streamline.apps.StreamlineConfig'