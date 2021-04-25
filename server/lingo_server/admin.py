from django.contrib.admin import ModelAdmin, register

from lingo_server.models import Language, Word, DictionaryVersion


@register(Language)
class LanguageAdmin(ModelAdmin):
    pass


@register(Word)
class WordAdmin(ModelAdmin):
    list_display = ('word', 'language', 'updated_at')


@register(DictionaryVersion)
class DictionaryVersionAdmin(ModelAdmin):
    fields = ('language', 'words', 'created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['words', 'created_at', 'updated_at', 'language']
        else:
            return ['words', 'created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.words = [
                word.word for word in Word.objects.order_by('word').filter(language_id=obj.language_id).all()
            ]

        super().save_model(request, obj, form, change)


class WordSuggestionAdmin(ModelAdmin):
    list_display = ('word', 'language', 'approved', 'rejected', 'created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        if obj.approved or obj.rejected:
            return ['words', 'created_at', 'updated_at', 'language', 'approved', 'rejected']
        else:
            return ['words', 'created_at', 'updated_at', 'language']
