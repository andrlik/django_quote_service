from django.contrib import admin

from .models import Character, CharacterGroup, CharacterMarkovModel, Quote

# Register your models here.


class CharacterGroupAdmin(admin.ModelAdmin):
    pass


class CharacterAdmin(admin.ModelAdmin):
    pass


class QuoteAdmin(admin.ModelAdmin):
    pass


class CharacterMarkovModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(CharacterGroup, CharacterGroupAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(CharacterMarkovModel, CharacterMarkovModelAdmin)
