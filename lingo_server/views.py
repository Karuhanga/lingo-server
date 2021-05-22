import json
from typing import List

from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from lingo_server.models import DictionaryVersion, Language, WordSuggestion


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
    words: List[str] = json.loads(request.body)['words']
    language = Language.objects.get(name=language_name)

    added_words = []
    for word in words:
        word, _ = WordSuggestion.objects.get_or_create(language=language, word=word)
        added_words.append(word.to_dict())

    return JsonResponse(dict(data=added_words))
