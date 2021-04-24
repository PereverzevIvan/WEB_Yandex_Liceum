from flask import Flask, url_for, render_template, request, redirect
import os
from random import choice
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
was_users = []


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/member', methods=['GET'])
def member():
    global was_users
    with open('templates/личная_карточка.json', mode='r', encoding='utf-8') as json_f:
        users = json.load(json_f)['users']
    user = choice(users)
    if len(was_users) == len(users):
        while user['name'] == was_users[-1]:
            user = choice(users)
        was_users = []
    else:
        while user['name'] in was_users:
            user = choice(users)
    was_users.append(user['name'])
    specialize = sorted(user['specialize'], key=lambda x: x)
    return render_template('личная_карточка.html', user=user, specialize=specialize)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
