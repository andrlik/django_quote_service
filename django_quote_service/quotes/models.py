import random
from typing import Optional, Any

import rules
from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from rules.contrib.models import RulesModelBase, RulesModelMixin
from slugify import slugify

from .markov_utils import MarkovPOSText
from .rules import (  # is_character_owner,; is_group_owner_and_authenticated,
    is_owner,
    is_owner_or_public,
)


class AbstractOwnerModel(models.Model):
    """
    Abstract model for representing an entity owned by a user with toggles for either allowing submissions for it
    and public access. Defaults to completely private by default.

    Attributes:
        public (bool): is this object public to any authenticated user? Default: False
        allow_submissions (bool): allow other users to submit child objects? Default: False. Not implemented yet.
        owner (User): The user that created this object.
    """

    public = models.BooleanField(
        default=False,
        help_text=_("Is this a public source available for any user to view?"),
    )
    allow_submissions = models.BooleanField(
        default=False, help_text=_("Allow submissions from other users?")
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


# Create your models here.
class CharacterGroup(
    AbstractOwnerModel, RulesModelMixin, TimeStampedModel, metaclass=RulesModelBase
):
    """
    An abstract group or source for a given set of quotes. Multiple sources, or Character objects, can belong to
    the same group.

    Attributes:
        id (int): Database primary key for the object.
        name (str): Human readable string to name the group. This will be converted to a slug prefix.
        description (str): A description of the group for convenience. Markdown can be used here for styling.
        description_rendered (str): The HTML representation of the description string. Generated automatically.
        owner (User): The user that created the group and therefore owns it.
        public (bool): Is this group public or private. Defaults to False.
        allow_submissions (bool): Allow other users to submit characters to this. Not yet implemented.
        slug (str): A unique slug to represent this group. Generated automatically from name.
        created (datetime): When this object was first created. Auto-generated.
        modified (datetime): Last time this object was modified. Auto-generated.

    """

    name = models.CharField(
        _("Source Name"),
        max_length=50,
        help_text=_(
            "A source for individuals making the quotes. Use as an abstract grouping."
        ),
        unique=True,
        db_index=True,
    )
    description = models.TextField(
        help_text=_("Description for the source. You can style using Markdown."),
        null=True,
        blank=True,
    )
    description_rendered = models.TextField(
        help_text=_("Automatically generated from description"), null=True, blank=True
    )
    slug = models.SlugField(
        unique=True,
        max_length=70,
        blank=True,
        help_text=_("Unique slug for this group."),
    )

    @cached_property
    def total_characters(self):
        return Character.objects.filter(group=self).count()

    @cached_property
    def markov_characters(self):
        return Character.objects.filter(group=self, allow_markov=True).count()

    def refresh_from_db(self, *args, **kwargs):
        super().refresh_from_db(*args, **kwargs)
        cached_properties = ["total_characters", "markov_characters"]
        for prop in cached_properties:
            try:
                del self.__dict__[prop]
            except KeyError:  # pragma: nocover
                pass

    def save(self, *args, **kwargs):
        if (
            not self.slug
        ):  # Once this slug is set, it does not change except through devil pacts
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):  # pragma: nocover
        return self.name

    class Meta:
        rules_permissions = {
            "add": rules.is_authenticated,
            "read": is_owner_or_public,
            "edit": is_owner,
            "delete": is_owner,
        }
        ordering = ["name"]


class Character(
    AbstractOwnerModel, RulesModelMixin, TimeStampedModel, metaclass=RulesModelBase
):
    """
    An individual character to attribute the quote to in the system.

    Attributes:
        id (int): Database primary key for the object.
        name (str): Unique name of a character within a ``CharacterGroup`` for this entity.
        group (CharacterGroup): The parent ``CharacterGroup``.
        slug (str): Slug made up of a generated version of the character name and the group slug prefix.
        description (str): Description for the character. Markdown can be used for styling.
        description_rendered (str): HTML representation of the description for convenience. Automatically generated.
        allow_markov (bool): Allow markov quotes to be requested from this character? Default False.
        owner (User): The user that created and owns this character.
        public (bool): Is the character public to other users? Defaults to False.
        allow_submissions (bool): Allow other users to submit quotes for this character? Defaults to False.
        created (datetime): When this object was first created. Auto-generated.
        modified (datetime): Last time this object was modified. Auto-generated.

    """

    name = models.CharField(max_length=100, help_text=_("Name of the character"))
    slug = models.SlugField(
        max_length=250,
        help_text=_(
            "Global slug of the character, will be auto generated from name and group if not overridden."
        ),
        blank=True,
        unique=True,
        db_index=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text=_("Description of this character. You can style this with Markdown."),
    )
    description_rendered = models.TextField(
        null=True, blank=True, help_text=_("Automatically generated from description.")
    )
    allow_markov = models.BooleanField(
        default=False, help_text=_("Allow to be used in markov chains?")
    )
    group = models.ForeignKey(
        CharacterGroup,
        on_delete=models.CASCADE,
        help_text=_("The group this character belongs to."),
    )

    @property
    def markov_ready(self) -> bool:
        """
        Conducts sanity checks to see if requesting a markov chain is feasible.
        :return: bool
        """
        if self.allow_markov and Quote.objects.filter(character=self).count() > 1:
            return True
        return False

    def get_markov_sentence(self, max_characters: Optional[int] = 280) -> Optional[str]:
        """
        If valid, generate a markov sentence. If not, return None.
        :param max_characters: Optional maximum limit of characters in the return set. Default: 280
        :return: str or None
        """
        if self.markov_ready:
            markov_model = CharacterMarkovModel.objects.get(character=self)
            if not markov_model.data:
                markov_model.generate_model_from_corpus()
            text_model = MarkovPOSText.from_json(markov_model.data)
            return text_model.make_short_sentence(max_chars=max_characters)
        return None

    def get_random_quote(
        self, max_quotes_to_process: Optional[int] = 50
    ) -> Optional[Any]:
        """
        This actually not all that random. It's going to grab the quotes
        ordered ordered by how infrequently they've been returned, and then grab a random one
        in the set. But for our purposes, it's fine. If there aren't any quotes, it will return None.
        :return: Quote object or None
        """
        quotes_to_pick = (
            Quote.objects.filter(character=self)
            .select_related("stats")
            .order_by("stats__times_used")[:max_quotes_to_process]
        )
        if quotes_to_pick.exists():
            # Select a random index in the result set.
            return random.choice(list(quotes_to_pick))
        return None

    def __str__(self):  # pragma: nocover
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{self.group.slug}-" + slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        rules_permissions = {
            "add": rules.is_authenticated,
            "read": is_owner_or_public,
            "edit": is_owner,
            "delete": is_owner,
        }


class Quote(
    AbstractOwnerModel, RulesModelMixin, TimeStampedModel, metaclass=RulesModelBase
):
    """
    A quote from a given character.

    Attributes:
        id (int): Database primary key for the object.
        quote (str): The quote text to use. You can use Markdown for styling. Must be <= 280 characters for tweets
        quote_rendered (str): HTML rendered version of the quote field. Automatically generated.
        citation (str): Optional description of quote source, e.g. episode number or book title.
        citation_url (str): Optional accompanying URL for the citation.
        character (Character): The character that said this quote.
        owner (User): The user that created and owns this quote.
        created (datetime): When this object was first created. Auto-generated.
        modified (datetime): Last time this object was modified. Auto-generated.

    """

    quote = models.CharField(
        max_length=280,  # Keep the base limit to 280 so that quotes are 'tweetable'
        help_text="Plain text representation of quote. You can use Markdown here.",
    )
    quote_rendered = models.TextField(
        null=True,
        blank=True,
        help_text=_("HTML rendered version of quote generated from quote plain text."),
    )
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, help_text=_("The character who said this.")
    )
    citation = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text=_("Where is this quote from? Episode #, book?"),
    )
    citation_url = models.URLField(
        null=True, blank=True, help_text=_("URL for citation, if applicable.")
    )

    def __str__(self):  # pragma: nocover
        return f"{self.character.name}: {self.quote}"

    class Meta:
        rules_permissions = {
            # "add": is_character_owner,
            "read": is_owner_or_public,
            "edit": is_owner,
            "delete": is_owner,
        }


class CharacterMarkovModel(TimeStampedModel):
    """
    The cached markov model for a given character. The databse object for this is automatically created
    whenever a new character object is saved.

    Attributes:
        id (int): Database primary key for the object.
        character (Character): The character who the model is sourced from.
        data (json): The JSON representation of the Markov model created by ``markovify``.
        created (datetime): When this object was first created. Auto-generated.
        modified (datetime): Last time this object was modified. Auto-generated.

    """

    character = models.OneToOneField(Character, on_delete=models.CASCADE)
    data = models.JSONField(null=True, blank=True)

    def generate_model_from_corpus(self):
        """
        Collect all quotes attributed to the related character. Then
        create, compile, and save the model.
        """
        quotes = Quote.objects.filter(character=self.character)
        # Don't bother generating model if there isn't data.
        if not quotes.exists():
            return  # pragma: nocover
        corpus = " ".join(quote.quote for quote in quotes)
        text_model = MarkovPOSText(corpus)
        text_model.compile(inplace=True)
        self.data = text_model.to_json()
        self.save()

    def __str__(self):  # pragma: nocover
        return self.character.name


class QuoteStats(TimeStampedModel):
    """
    A simple object used to track how often an individual quote is used.

    Attributes:
        id (int): The database primary key of this object.
        quote (Quote): The quote this stat relates to.
        times_used (int): The number of times this has been used by an service such as random quote.
        created (datetime): When this was created.
        modified (datetime): When this was last modified.
    """

    quote = models.OneToOneField(
        Quote,
        on_delete=models.CASCADE,
        related_name="stats",
        help_text=_("The Quote the stats related to."),
    )
    times_used = models.PositiveIntegerField(
        default=0, help_text=_("Times used for random quotes, etc.")
    )

    def __str__(self):  # pragma: nocover
        return f"Stats for Quote {self.quote.id}"


class GroupStats(TimeStampedModel):
    """
    An object for using to track usage stats for ``CharacterGroup``.

    Attributes:
        group (CharacterGroup): The group this is collecting stats for.
        quotes_requested (int): The number of times a quote from this object or its children has been requested.
        quotes_generated (int): The number of times a markov quote has been generated for this or it's children.
    """

    group = models.OneToOneField(
        CharacterGroup, related_name="stats", on_delete=models.CASCADE
    )
    quotes_requested = models.PositiveIntegerField(
        default=0, help_text=_("Number of time child quotes have been requested.")
    )
    quotes_generated = models.PositiveIntegerField(
        default=0,
        help_text=_("Number of times markov generated quotes have been requested."),
    )


class CharacterStats(TimeStampedModel):
    """
    An object for using to track usage stats for ``Character``.

    Attributes:
        character (Character): The character this is collecting stats for.
        quotes_requested (int): The number of times a quote from this object or its children has been requested.
        quotes_generated (int): The number of times a markov quote has been generated for this or it's children.
    """

    character = models.OneToOneField(
        Character, related_name="stats", on_delete=models.CASCADE
    )
    quotes_requested = models.PositiveIntegerField(
        default=0, help_text=_("Number of time child quotes have been requested.")
    )
    quotes_generated = models.PositiveIntegerField(
        default=0,
        help_text=_("Number of times markov generated quotes have been requested."),
    )
