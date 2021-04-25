from django.contrib.admin import ModelAdmin, register, action, site
from django.core.checks import messages

from lingo_server.models import Language, Word, DictionaryVersion, WordSuggestion


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


@register(WordSuggestion)
class WordSuggestionAdmin(ModelAdmin):
    list_display = ('word', 'language', 'was_reviewed', 'approved', 'rejected', 'created_at', 'updated_at')
    fields = ('language', 'word', 'was_reviewed', 'approved', 'rejected', 'created_at', 'updated_at')
    actions = ['approve', 'reject']

    @action(description='Approve selected words')
    def approve(self, request, queryset):
        suggestions = queryset.all()
        for suggestion in suggestions:
            if suggestion.was_reviewed_bool():
                return self.message_user(
                    request, "Cannot approve already reviewed words. Please deselect them.", level=messages.ERROR
                )

        Word.objects.bulk_create(
            [Word(word=suggestion.word, language=suggestion.language) for suggestion in suggestions],
            ignore_conflicts=True,
        )
        queryset.update(approved=True)

    @action(description='Reject selected words')
    def reject(self, request, queryset):
        suggestions = queryset.all()
        for suggestion in suggestions:
            if suggestion.was_reviewed_bool():
                return self.message_user(
                    request, "Cannot reject already reviewed words. Please deselect them.", level=messages.ERROR
                )

        queryset.update(rejected=True)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['word', 'created_at', 'updated_at', 'language', 'approved', 'rejected', 'was_reviewed']
        else:
            return ['created_at', 'updated_at', 'approved', 'rejected', 'was_reviewed']


site.site_header = 'Lingo Admin'
site.index_title = 'Lingo Admin'
site.site_title = 'Lingo Admin'
