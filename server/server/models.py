from django.db.models import Model, CharField, ForeignKey, JSONField, DateTimeField, CASCADE


class Language(Model):
    name = CharField("Language Name", max_length=100, unique=True, null=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Word(Model):
    class Meta:
        unique_together = ('word', 'language')

    word = CharField(max_length=100, null=False)
    language = ForeignKey(Language, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class DictionaryVersion(Model):
    words = JSONField(null=False)
    language = ForeignKey(Language, on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
