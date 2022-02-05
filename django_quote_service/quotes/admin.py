from django.contrib import admin

from .models import Character, CharacterGroup, Quote

# Register your models here.


class CharacterGroupAdmin(admin.ModelAdmin):
    pass


class CharacterAdmin(admin.ModelAdmin):
    pass


class QuoteAdmin(admin.ModelAdmin):
    pass


admin.site.register(CharacterGroup, CharacterGroupAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Quote, QuoteAdmin)
