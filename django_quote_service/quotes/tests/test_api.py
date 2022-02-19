import pytest
from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..api.serializers import CharacterSerializer
from ..api.views import CharacterGroupViewSet
from ..models import CharacterGroup

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def apiclient():
    return APIClient()


class TestGroupViewSet:
    def test_list_groups(
        self, property_group: CharacterGroup, rf: RequestFactory
    ) -> None:
        view = CharacterGroupViewSet()
        request = rf.get("/ignorethisurl/")
        request.user = property_group.owner
        view.request = request
        assert property_group in view.get_queryset()

    def test_retrieve_group(self, apiclient, property_group):
        apiclient.force_authenticate(user=property_group.owner)
        response = apiclient.get(
            reverse("api:group-detail", kwargs={"group": property_group.slug}),
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_random_quote(self, apiclient, property_group):
        apiclient.force_authenticate(user=property_group.owner)
        response = apiclient.get(
            reverse(
                "api:group-get-random-quote",
                kwargs={"group": property_group.slug},
            )
        )
        assert response.status_code == status.HTTP_200_OK

    def test_markov_group(self, apiclient, property_group):
        apiclient.force_authenticate(user=property_group.owner)
        response = apiclient.get(
            reverse(
                "api:group-generate-sentence", kwargs={"group": property_group.slug}
            )
        )
        assert response.status_code == status.HTTP_200_OK


class TestCharacterViewSet:
    def test_list_characters(self, apiclient, property_group):
        apiclient.force_authenticate(user=property_group.owner)
        response = apiclient.get(reverse("api:character-list"))
        assert response.status_code == status.HTTP_200_OK

    def test_list_characters_by_group(self, apiclient, property_group):
        apiclient.force_authenticate(user=property_group.owner)
        response = apiclient.get(
            reverse("api:character-list"), group=property_group.slug
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_character(self, apiclient, property_group):
        char_to_retrieve = property_group.character_set.all()[0]
        serializer = CharacterSerializer(char_to_retrieve)
        apiclient.force_authenticate(user=property_group.owner)
        response = apiclient.get(
            reverse("api:character-detail", kwargs={"character": char_to_retrieve.slug})
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data == serializer.data

    def test_character_random_quote(self, apiclient, property_group):
        char_to_retrieve = property_group.character_set.all()[0]
        apiclient.force_authenticate(user=property_group.owner)
        response = apiclient.get(
            reverse(
                "api:character-get-random-quote",
                kwargs={"character": char_to_retrieve.slug},
            )
        )
        assert response.status_code == status.HTTP_200_OK

    def test_character_generate_sentence(self, apiclient, property_group):
        char_to_retrieve = property_group.character_set.filter(allow_markov=True)[0]
        apiclient.force_authenticate(user=property_group.owner)
        response = apiclient.get(
            reverse(
                "api:character-generate-sentence",
                kwargs={"character": char_to_retrieve.slug},
            )
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["sentence"] is not None
