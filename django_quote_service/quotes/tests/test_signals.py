import pytest

from ...users.models import User
from ..models import (
    Character,
    CharacterGroup,
    CharacterMarkovModel,
    CharacterStats,
    GroupStats,
    Quote,
    QuoteStats,
)

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


def test_character_creation_allow_creates_markov_model_object(user: User) -> None:
    """
    Test that creating a character also creates it's related markov model with initially empty data.
    """
    group = CharacterGroup.objects.create(name="Monkey", owner=user)
    character = Character.objects.create(name="Curious George", group=group, owner=user)
    assert CharacterMarkovModel.objects.get(character=character)


def test_character_group_creation_generates_stats_object(user: User) -> None:
    """
    Test that the creation of either a character group or character creates its related
    stats object.
    """
    group = CharacterGroup.objects.create(name="Monkey", owner=user)
    assert GroupStats.objects.get(group=group)
    character = Character.objects.create(name="Curious George", group=group, owner=user)
    assert CharacterStats.objects.get(character=character)
    quote = Quote.objects.create(
        quote="I'm all a twitter.", character=character, owner=user
    )
    assert QuoteStats.objects.get(quote=quote)
