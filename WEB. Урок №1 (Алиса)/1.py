from flask import Flask, request
import logging
import json

IS_BUY = False

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {'end_session': False}}
    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')
    return json.dumps(response)


def handle_dialog(req, res):
    global IS_BUY
    user_id = req['session']['user_id']
    animal = 'слон' if not IS_BUY else 'крол'
    if req['session']['new']:
        sessionStorage[user_id] = {'suggests': ["Не хочу.", "Не буду.", "Отстань!"]}
        res['response']['text'] = f'Привет! Купи {animal}а!'
        res['response']['buttons'] = get_suggests(user_id)
        return
    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
        'я покупаю',
        'я куплю'
    ]:
        IS_BUY = not IS_BUY
        animal = 'слон' if not IS_BUY else 'крол'
        if not IS_BUY:
            res['response']['text'] = f'{animal.capitalize()} можно найти в Яндекс.Маркете!'
            res['response']['end_session'] = True
        else:
            sessionStorage[user_id] = {'suggests': ["Не хочу.", "Не буду.", "Отстань!"]}
            res['response']['text'] = f'Привет! Купи {animal}а!'
            res['response']['buttons'] = get_suggests(user_id)
        return
    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи {animal}а!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    animal = 'слон' if not IS_BUY else 'крол'
    session = sessionStorage[user_id]
    suggests = [
        {'title': suggest, 'hide': True} for suggest in session['suggests'][:2]]
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": f"https://market.yandex.ru/search?text={animal}ик",
            "hide": True})
    return suggests


if __name__ == '__main__':
    app.run()
