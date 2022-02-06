import pytest

from ...users.models import User
from ..models import Character, CharacterGroup, Quote

pytestmark = pytest.mark.django_db(transaction=True)


def test_charactergroup_description_render(user: User) -> None:
    """
    Test that a description on character group triggers markdown generation.
    :param user: Logged in user.
    :return:
    """
    group = CharacterGroup.objects.create(name="Monkey", owner=user)
    assert group.description is None and group.description == group.description_rendered
    group.description = "A **dark** time for all."
    group.save()
    assert group.description_rendered == "<p>A <strong>dark</strong> time for all.</p>"
    group.description = None
    group.save()
    assert group.description_rendered is None


def test_character_description_render(user: User) -> None:
    """
    Test that a description on a character triggers markdown version.
    :param user:
    :return:
    """
    group = CharacterGroup.objects.create(name="Monkey", owner=user)
    character = Character.objects.create(name="Curious George", group=group, owner=user)
    assert (
        character.description is None
        and character.description_rendered == character.description
    )
    character.description = "A **dark** time for all."
    character.save()
    assert (
        character.description_rendered == "<p>A <strong>dark</strong> time for all.</p>"
    )
    character.description = None
    character.save()
    assert character.description_rendered is None


def test_quote_rendering(user: User) -> None:
    """
    Test that quotes get properly formatted as markdown.
    :param user: The logged in user
    :return:
    """
    group = CharacterGroup.objects.create(name="Monkey", owner=user)
    character = Character.objects.create(name="Curious George", group=group, owner=user)
    # Quotes can never be none so we just have to verify that the rendered version is getting created.
    quote = Quote.objects.create(
        character=character, owner=user, quote="A **dark** time for all."
    )
    assert quote.quote_rendered == "<p>A <strong>dark</strong> time for all.</p>"
