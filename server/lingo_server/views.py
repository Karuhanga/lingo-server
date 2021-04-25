import json

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
def suggest_word(request: HttpRequest, language_name: str):
    word = json.loads(request.body)['word']
    language = Language.objects.get(name=language_name)
    word, _ = WordSuggestion.objects.get_or_create(language=language, word=word)

    return JsonResponse(dict(data=word.to_dict()))
