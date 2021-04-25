from django.http import JsonResponse, HttpRequest

from lingo_server.models import DictionaryVersion


def dictionary_version_is_latest(request: HttpRequest, dictionary_id: int):
    language = DictionaryVersion.objects.filter(id=dictionary_id)
    is_latest = DictionaryVersion.objects.filter(language=language).order_by('-created_at').first().id == dictionary_id
    return JsonResponse(dict(data=is_latest))


def latest_dictionary(request, language_name: str):
    dictionary_version = DictionaryVersion.objects.filter(language__name=language_name).order_by('-created_at').first()
    return JsonResponse(dict(data=dictionary_version.to_dict()))
