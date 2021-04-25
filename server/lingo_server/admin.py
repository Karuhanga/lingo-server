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
    readonly_fields = ('words', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.words = [
                word.word for word in Word.objects.order_by('word').filter(language_id=obj.language_id).all()
            ]

        super().save_model(request, obj, form, change)
