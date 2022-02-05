from django.db.models.signals import pre_save
from django.dispatch import receiver
from markdown import markdown

from .models import Character, CharacterGroup, Quote


@receiver(pre_save, sender=CharacterGroup)
@receiver(pre_save, sender=Character)
def render_description(sender, instance, *args, **kwargs):
    """
    Automatically renders the description from markdown.
    """
    if instance.description is not None:
        instance.description_rendered = markdown(instance.description)
    else:
        instance.description_rendered = None


@receiver(pre_save, sender=Quote)
def render_quote(sender, instance, *args, **kwargs):
    """
    Render the quote via markdown and save the results.
    """
    instance.quote_rendered = markdown(instance.quote)
