from django.db.models import Model, CharField, ForeignKey, JSONField, DateTimeField, CASCADE, BooleanField

from lingo_server.utiils.model_utils import LowerCaseCharField


class Language(Model):
    name = CharField("Language Name", max_length=100, unique=True, null=False, db_index=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AbstractWord(Model):
    class Meta:
        unique_together = ('word', 'language')
        abstract = True

    word = LowerCaseCharField(max_length=100, null=False, db_index=True)
    language = ForeignKey(Language, on_delete=CASCADE, db_index=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.word

    def to_dict(self):
        return dict(
            id=self.id,
            word=self.word,
            language=self.language.name,
        )


class Word(AbstractWord):
    pass


class DictionaryVersion(Model):
    class Meta:
        verbose_name = "Dictionary Version"

    words = JSONField(null=False)
    language = ForeignKey(Language, on_delete=CASCADE, db_index=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.language}/{self.created_at.strftime('%Y/%m/%d')}-{self.id}"

    def to_dict(self):
        return dict(
            id=self.id,
            words=self.words,
            language=self.language.name,
        )


class WordSuggestion(AbstractWord):
    class Meta:
        verbose_name = "Word Suggestion"

    approved = BooleanField(null=True)
    rejected = BooleanField(null=True)

    def was_reviewed_bool(self):
        return self.approved or self.rejected

    @property
    def was_reviewed(self):
        return 'Yes' if self.was_reviewed_bool() else 'No'
