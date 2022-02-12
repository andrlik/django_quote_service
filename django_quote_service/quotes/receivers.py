from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from markdown import markdown

from .models import (
    Character,
    CharacterGroup,
    CharacterMarkovModel,
    CharacterStats,
    GroupStats,
    Quote,
    QuoteStats,
)


@receiver(pre_save, sender=CharacterGroup)
@receiver(pre_save, sender=Character)
def render_description(sender, instance, *args, **kwargs):
    """
    Automatically renders the description from markdown.
    """
    if instance.description:
        instance.description_rendered = markdown(instance.description)
    else:
        instance.description_rendered = None


@receiver(pre_save, sender=Quote)
def render_quote(sender, instance, *args, **kwargs):
    """
    Render the quote via markdown and save the results.
    """
    instance.quote_rendered = markdown(instance.quote)


@receiver(post_save, sender=Character)
def initialize_markov_object(sender, instance, created, *args, **kwargs):
    """
    Creates the one-to-one object to accompany the character object.
    """
    if created:
        CharacterMarkovModel.objects.create(character=instance)


@receiver(post_save, sender=CharacterGroup)
@receiver(post_save, sender=Character)
@receiver(post_save, sender=Quote)
def initialize_grouping_stat_object(sender, instance, created, *args, **kwargs):
    """
    Creates the initial stat objects in the database.
    """
    if created:
        if sender == CharacterGroup:
            GroupStats.objects.create(group=instance)
        elif sender == Character:
            CharacterStats.objects.create(character=instance)
        elif sender == Quote:
            QuoteStats.objects.create(quote=instance)
