from django.contrib.admin import ModelAdmin, register

from lingo_server.models import Language, Word, DictionaryVersion


@register(Language)
class LanguageAdmin(ModelAdmin):
    pass


@register(Word)
class WordAdmin(ModelAdmin):
    pass


@register(DictionaryVersion)
class DictionaryVersionAdmin(ModelAdmin):
    pass
