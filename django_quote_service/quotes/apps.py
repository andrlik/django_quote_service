from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QuotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_quote_service.quotes"
    verbose_name = _("Quotes")

    def ready(self):
        try:
            import django_quote_service.quotes.receivers  # noqa F401
        except ImportError:
            pass
