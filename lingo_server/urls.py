"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from lingo_server.views import dictionary_version_is_latest, latest_dictionary_version, suggest_words, WordsView

urlpatterns = [
    path('dictionaries/versions/<int:dictionary_version_id>/is_latest', dictionary_version_is_latest),
    path('languages/<str:language_name>/dictionaries/versions/latest', latest_dictionary_version),
    path('languages/<str:language_name>/suggestions', suggest_words),
    path('languages/<str:language_name>/words', WordsView.as_view()),
]
