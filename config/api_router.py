from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from django_quote_service.quotes.api.views import (
    CharacterGroupViewSet,
    CharacterViewSet,
)
from django_quote_service.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("groups", CharacterGroupViewSet, basename="group")
router.register("characters", CharacterViewSet, basename="character")


app_name = "api"
urlpatterns = router.urls
