from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class QuotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_quote_service.quotes"
    verbose_name = _("Quotes")
