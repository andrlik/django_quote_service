import rules
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from rules.contrib.models import RulesModelBase, RulesModelMixin
from slugify import slugify

from .rules import (  # is_character_owner,; is_group_owner_and_authenticated,
    is_owner,
    is_owner_or_public,
)


class AbstractOwnerModel(models.Model):
    """
    Abstract model for representing an entity owned by a user with toggles for either allowing submissions for it
    and public access. Defaults to completely private by default.
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
    An abstract group or source for a given set of quotes.
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
    """

    name = models.CharField(max_length=100, help_text=_("Name of the character"))
    slug = models.SlugField(
        max_length=250,
        help_text=_(
            "Global slug of the character, will be auto generated from name and group if not overriden."
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

    def __str__(self):  # pragma: nocover
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.group.name} {self.name}")
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
    """

    quote = models.TextField(
        help_text="Plain text representation of quote. You can use Markdown here."
    )
    quote_rendered = models.TextField(
        null=True,
        blank=True,
        help_text=_("HTML rendered version of quote generated from quote plain text."),
    )
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, help_text=_("The character who said this.")
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
    character = models.OneToOneField(Character, on_delete=models.CASCADE)
    data = models.JSONField(null=True, blank=True)

    def __str__(self):  # pragma: nocover
        return self.character.name
