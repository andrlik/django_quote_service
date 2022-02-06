import pytest
from django.db import IntegrityError

from ...users.models import User
from ..models import Character, CharacterGroup

pytestmark = pytest.mark.django_db(transaction=True)


def test_generate_slug(user: User) -> None:
    """
    Tests the slug generation for characters to ensure it's being set up correctly.

    :param user: The user who is currently logged in.
    :return:
    """
    group = CharacterGroup.objects.create(name="Monkey", owner=user)
    character = Character.objects.create(name="John Smith", group=group, owner=user)
    assert character.slug == "monkey-john-smith"


@pytest.mark.parametrize(
    "group1,group2,character_name,slug",
    [
        ("EW", "Ew", "John Smith", "ew-john-smith"),
        ("EW", "Explorers Wanted", "John Smith", "ew-john-smith"),
    ],
)
def test_reject_duplicate_slug(
    user: User, group1: str, group2: str, character_name: str, slug: str
) -> None:
    """
    :param group1: Name of the first group
    :param group2: Name of the second group
    :param character_name: Name of the character.
    :param slug: Slug to override.
    :param user: The user who is currently logged in.
    :return:
    """
    group = CharacterGroup.objects.create(name=group1, owner=user)
    Character.objects.create(name=character_name, group=group, owner=user)
    group2 = CharacterGroup.objects.create(name=group2, owner=user)
    with pytest.raises(IntegrityError):
        Character.objects.create(
            name=character_name, group=group2, slug=slug, owner=user
        )
