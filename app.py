from flask import Flask, render_template, request, send_from_directory

import requests
import logging
import os

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='templates/', )


API_BASE_URL = os.environ.get('API_BASE_URL')


@app.route('/<path:filename>')
def templates_static(filename):
    """Indicates that the statics files are in the same level as root"""
    return send_from_directory('templates', filename)


@app.route('/')
def home():
    """Loads main page"""
    language = request.accept_languages.best
    words_to_translate = ["our_company", "our_work",
                          "gallery", "contact", "openingtext", "think_of_an_idea",
                          "discuss_pros_and_cons", "create_it", "start_working_we_help",
                          "execute_it", "roll_and_correct", "dont_know_what_to_put_here",
                          "see_more", "contact_us", "name", "email", "message", "send"]
    translation = get_translation_from_api(words_to_translate, language)
    return render_template('index.html', translation=translation)


def get_translation_from_api(words, language):
    url = f"{API_BASE_URL}/language/{language}"
    response = requests.post(url, json=words)
    if response.status_code == 200:
        data = response.json()
        result = data['translations']

        # If not all the words have translation...
        if len(words) > len(result):
            missing_words = set(words) - set(result.keys())

            # I fill the remaining with the same as origin.
            for word in missing_words:
                result[word] = word

        return result
    else:
        result = {}
        for word in words:
            result[word] = word
        return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
