import json
from typing import List, Type

from django.http import JsonResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import View

from lingo_server.models import DictionaryVersion, Language, WordSuggestion, Word, AbstractWord
from server.auth import has_auth_token


@require_http_methods(["GET"])
def dictionary_version_is_latest(request: HttpRequest, dictionary_version_id: int):
    dictionary_version = DictionaryVersion.objects.get(id=dictionary_version_id)
    is_latest = DictionaryVersion.objects.filter(language=dictionary_version.language).order_by('-created_at').first().id == dictionary_version_id
    return JsonResponse(dict(data=dict(is_latest=is_latest)))


@require_http_methods(["GET"])
def latest_dictionary_version(request: HttpRequest, language_name: str):
    dictionary_version = DictionaryVersion.objects.filter(language__name=language_name).order_by('-created_at').first()
    return JsonResponse(dict(data=dictionary_version.to_dict()))


@csrf_exempt
@require_http_methods(["POST"])
def suggest_words(request: HttpRequest, language_name: str):
    return create_words(request, language_name, WordSuggestion)


@method_decorator(csrf_exempt, name='dispatch')
class WordsView(View):
    @staticmethod
    @has_auth_token
    def delete(request: HttpRequest, language_name: str):
        Word.objects.filter(language__name=language_name).all().delete()
        return JsonResponse(dict(message="Done!"))

    @staticmethod
    @has_auth_token
    def post(request: HttpRequest, language_name: str):
        return create_words(request, language_name, Word)


def create_words(request: HttpRequest, language_name: str, word_type: Type[AbstractWord]):
    words: List[str] = json.loads(request.body)['words']
    language = Language.objects.get(name=language_name)

    added_words = []
    for word in words:
        word, _ = word_type.objects.get_or_create(language=language, word=word)
        added_words.append(word.to_dict())

    return JsonResponse(dict(data=added_words))
