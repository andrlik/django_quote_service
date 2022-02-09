from django.urls import path

from .views import (
    CharacterGroupCreateView,
    CharacterGroupDeleteView,
    CharacterGroupDetailView,
    CharacterGroupListView,
    CharacterGroupUpdateView,
)

app_name = "quotes"
urlpatterns = [
    path("groups/", view=CharacterGroupListView.as_view(), name="group_list"),
    path(
        "groups/create/", view=CharacterGroupCreateView.as_view(), name="group_create"
    ),
    path(
        "groups/<int:id>/", view=CharacterGroupDetailView.as_view(), name="group_detail"
    ),
    path(
        "groups/<int:id>/", view=CharacterGroupUpdateView.as_view(), name="group_update"
    ),
    path(
        "groups/<int:id>/delete/",
        view=CharacterGroupDeleteView.as_view(),
        name="group_delete",
    ),
]
