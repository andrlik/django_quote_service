from django.conf import settings
from django_quotes.api.views import SourceGroupViewSet, SourceViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

from django_quote_service.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("groups", SourceGroupViewSet, basename="group")
router.register("sources", SourceViewSet, basename="source")


app_name = "api"
urlpatterns = router.urls
