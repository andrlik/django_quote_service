from rest_framework.serializers import ModelSerializer

from ..models import Character, CharacterGroup, Quote


class CharacterSerializer(ModelSerializer):
    class Meta:
        model = Character
        fields = ["name", "group", "description", "description_rendered"]


class CharacterGroupSerializer(ModelSerializer):
    class Meta:
        model = CharacterGroup
        fields = ["name", "slug", "description", "description_rendered"]


class QuoteSerializer(ModelSerializer):
    class Meta:
        model = Quote
        fields = ["quote", "quote_rendered", "character"]
