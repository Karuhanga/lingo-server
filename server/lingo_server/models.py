from django.db.models import Model, CharField, ForeignKey, JSONField, DateTimeField, CASCADE


class Language(Model):
    name = CharField("Language Name", max_length=100, unique=True, null=False, db_index=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Word(Model):
    class Meta:
        unique_together = ('word', 'language')

    word = CharField(max_length=100, null=False, db_index=True)
    language = ForeignKey(Language, on_delete=CASCADE, db_index=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.word


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
