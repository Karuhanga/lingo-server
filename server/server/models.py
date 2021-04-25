from django.db.models import Model, CharField, ForeignKey, CASCADE


class Language(Model):
    name = CharField("Language Name", max_length=100)


class Word(Model):
    word = CharField(max_length=100)
    language = ForeignKey(Language, on_delete=CASCADE)
