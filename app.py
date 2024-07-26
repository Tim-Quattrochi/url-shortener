
from flask import Flask, redirect, request, jsonify, render_template, url_for
import os
from dotenv import load_dotenv


app = Flask(__name__)


load_dotenv()

url_dict = {
    '1': 'https://www.google.com',
    '2': 'https://www.yahoo.com',
    '3': 'https://www.cnn.com',
    '4': 'https://www.bbc.com',
    '5': 'https://www.espn.com'
}


valid_api_key = os.getenv('API_KEY')


def is_api_key_valid_and_set(request):
    api_key = request.headers.get(
        'API-KEY') or request.headers.get('Api-Key')
    return api_key == valid_api_key and valid_api_key is not None


@app.route('/')
def index():
    return render_template('index.html', title='Home', message='Welcome to the URL Shortener!')


@app.route('/<short_code>')
def allow(short_code):

    print("The short_code was: ", short_code)

    for key in url_dict:
        if key == short_code:
            return redirect(url_dict[short_code], code=301)
        else:
            return render_template('allow.html')


@app.route('/url', methods=['POST'])
def crud_api_post():
    if is_api_key_valid_and_set(request) is False:
        return jsonify({'error': 'Invalid API-KEY'}), 401

    if request.method == 'POST':
        data = request.json
        code = data.get('code')
        url = data.get('url')

        if code in url_dict:
            return jsonify({'error': code + ' already exists!'}), 409
        else:
            url_dict[code] = url
            return jsonify({'data': code, 'url': url_dict[code]}), 201


@app.route('/url/<short_code>', methods=['DELETE', 'GET'])
def crud_api_delete(short_code):
    if is_api_key_valid_and_set(request) is False:
        return jsonify({'error': 'Invalid API-KEY'}), 401

    if request.method == 'GET':
        if short_code in url_dict:
            return redirect(url_dict[short_code], code=301)
        else:
            return render_template('allow.html')

    if request.method == 'DELETE':
        if short_code in url_dict:
            del url_dict[short_code]
            return jsonify({'message': 'Short code deleted'}), 200
        else:
            return jsonify({'error': 'Short code not found'}), 404


if __name__ == '__main__':

    app.run(host="0.0.0.0", port=80)
