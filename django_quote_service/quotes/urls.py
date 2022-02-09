from django.urls import path

from .views import (
    CharacterGroupCreateView,
    CharacterGroupDeleteView,
    CharacterGroupDetailView,
    CharacterGroupListView,
    CharacterGroupUpdateView,
    CharacterListView,
    CharacterCreateView,
    CharacterUpdateView,
    CharacterDetailView,
    CharacterDeleteView,
    QuoteListView,
    QuoteCreateView,
    QuoteDetailView,
    QuoteUpdateView,
    QuoteDeleteView,
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
        "groups/<int:id>/edit/",
        view=CharacterGroupUpdateView.as_view(),
        name="group_update",
    ),
    path(
        "groups/<int:id>/delete/",
        view=CharacterGroupDeleteView.as_view(),
        name="group_delete",
    ),
    path(
        "groups/<int:group>/characters/",
        view=CharacterListView.as_view(),
        name="character_list",
    ),
    path(
        "groups/<int:group>/characters/add/",
        view=CharacterCreateView.as_view(),
        name="character_create",
    ),
    path(
        "characters/<slug:slug>/",
        view=CharacterDetailView.as_view(),
        name="character_detail",
    ),
    path(
        "characters/<slug:slug>/edit/",
        view=CharacterUpdateView.as_view(),
        name="character_update",
    ),
    path(
        "characters/<slug:slug>/delete/",
        view=CharacterDeleteView.as_view(),
        name="character_delete",
    ),
    path(
        "characters/<slug:character>/quotes/",
        view=QuoteListView.as_view(),
        name="quote_list",
    ),
    path(
        "characters/<slug:character>/quotes/add/",
        view=QuoteCreateView.as_view(),
        name="quote_create",
    ),
    path("quotes/<int:id>/", view=QuoteDetailView.as_view(), name="quote_detail"),
    path("quotes/<int:id>/edit/", view=QuoteUpdateView.as_view(), name="quote_update"),
    path(
        "quotes/<int:id>/delete/", view=QuoteDeleteView.as_view(), name="quote_delete"
    ),
]
