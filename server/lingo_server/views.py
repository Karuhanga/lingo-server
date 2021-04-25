from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods

from lingo_server.models import DictionaryVersion, Language, WordSuggestion


@require_http_methods(["GET"])
def dictionary_version_is_latest(request: HttpRequest, dictionary_id: int):
    dictionary_version = DictionaryVersion.objects.filter(id=dictionary_id)
    is_latest = DictionaryVersion.objects.filter(language=dictionary_version).order_by('-created_at').first().id == dictionary_id
    return JsonResponse(dict(data=is_latest))


@require_http_methods(["GET"])
def latest_dictionary(request: HttpRequest, language_name: str):
    dictionary_version = DictionaryVersion.objects.filter(language__name=language_name).order_by('-created_at').first()
    return JsonResponse(dict(data=dictionary_version.to_dict()))


@require_http_methods(["POST"])
def suggest_word(request: HttpRequest, language_name: str):
    word = request.POST['word']
    language = Language.objects.filter(name=language_name).one()
    word, _ = WordSuggestion.objects.get_or_create(language=language, word=word)

    return JsonResponse(dict(data=word.to_dict()))
