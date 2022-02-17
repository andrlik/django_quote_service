from django.db import transaction
from django.db.models import F
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from markdown import markdown

from .models import (
    Character,
    CharacterGroup,
    CharacterMarkovModel,
    CharacterStats,
    GroupMarkovModel,
    GroupStats,
    Quote,
    QuoteStats,
)
from .signals import markov_sentence_generated, quote_random_retrieved


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


@receiver(post_save, sender=CharacterGroup)
def initialize_group_markov_object(sender, instance, created, *args, **kwargs):
    """
    Creates the one-to-one object for the group markov model.
    """
    if created:
        GroupMarkovModel.objects.create(group=instance)


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


@receiver(quote_random_retrieved, sender=Character)
def update_stats_for_quote_character(
    sender, instance, quote_retrieved, *args, **kwargs
):
    """
    Update the stats for the character, character group, and quote for a random retrieval.
    :param sender: Usually a character or character group class.
    :param instance: The Character this was generated for.
    :param quote_retrieved: The quote that was returned.
    :return: None
    """
    group_stats = instance.group.stats
    character_stats = instance.stats
    quote_stats = quote_retrieved.stats
    with transaction.atomic():
        group_stats.quotes_requested = F("quotes_requested") + 1
        group_stats.save()
        character_stats.quotes_requested = F("quotes_requested") + 1
        character_stats.save()
        quote_stats.times_used = F("times_used") + 1
        quote_stats.save()


@receiver(markov_sentence_generated, sender=Character)
def update_stats_for_markov(sender, instance, *args, **kwargs):
    """
    For a given character, update the stats on the Character and CharacterGroup for markov requests.
    :param sender: The requesting class, usually Character.
    :param instance: The specific character requested.
    :return: None
    """
    group_stats = instance.group.stats
    character_stats = instance.stats
    with transaction.atomic():
        group_stats.quotes_generated = F("quotes_generated") + 1
        group_stats.save()
        character_stats.quotes_generated = F("quotes_generated") + 1
        character_stats.save()
