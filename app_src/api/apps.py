from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ApiConfig(AppConfig):
    name = "app_src.api"
    verbose_name = _("Api")

    def ready(self):
        try:
            import app_src.api.signals  # noqa F401
        except ImportError:
            pass
