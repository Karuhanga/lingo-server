import math

import requests


def load_dictionary(host, token, language_name, words_file):
    if not "y" == input(f"🚀 with host: {host}, language: {language_name} and file: {words_file}. Are you sure? [y/N]").strip().lower():
        return print("Aborted.")

    endpoint = f"{host}/languages/{language_name}/words"
    headers = dict(Authorization=f"Bearer {token}")

    print(f"Nuking {language_name} dictionary...")
    requests.delete(endpoint, headers=headers)

    with open(words_file, "r") as file:
        words = file.read().splitlines(keepends=False)

    batches_of = 200
    at = 0
    total_words = len(words)
    while at < total_words:
        print(f"Sending batch {at//batches_of + 1} of {math.ceil(total_words/batches_of)}...")

        requests.post(endpoint, dict(words=words[at:at+batches_of]), headers=headers)
        at += batches_of

    print("Done 🎉")
