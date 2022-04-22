from flask import Flask, request
import logging
import json
import random
from texts import *

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# Создаем словарь, где для каждого пользователя
# мы будем хранить его имя
sessionStorage = {}




@app.route('/', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        # создаем словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'first_name': None,
            'action': False,
            'danetka': False
        }
        return

    # Если пользователь не новый, то попадаем сюда.
    # Если поле имени пустое, то это говорит о том,
    # что пользователь еще не представился.
    if sessionStorage[user_id]['first_name'] is None:
        # В последнем его сообщение ищем имя.
        first_name = get_first_name(req)
        # Если не нашли, то сообщаем пользователю, что не расслышали.
        if first_name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        # Если нашли, то приветствуем пользователя
        # и спрашиваем знает ли он правила
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response']['text'] = 'Приятно познакомиться, ' + first_name.title() + '. Я - Алиса. Ты знаешь правила игры?'
            return
    else:
        if req['request']['original_utterance'].lower() in help:
            res['response']['text'] = rules
            return

        if sessionStorage[user_id]['action'] == 'exit':
            if not yes_or_no(req, res):
                res['response']['text'] = 'До встречи'
                res['response']['end_session'] = True
                return
            else:
                sessionStorage[user_id]['action'] = False

        if not sessionStorage[user_id]['action']:
            if yes_or_no(req, res):
                res['response']['text'] = 'Хорошо! Тогда давай играть, выбери Данетку:\n'
                logging.info(str([e for e in Danetki.keys()][2:-2]))
                res['response']['text'] += str([e for e in Danetki.keys()])[2:-2]
                sessionStorage[user_id]['action'] = 'select'  # добавляем в sessionStorage action!!!
            else:
                res['response']['text'] = rules + 'Давай играть?'
                sessionStorage[user_id]['action'] = 'exit'
            return

        if sessionStorage[user_id]['action'] == 'select':
            if req['request']['original_utterance'] in Danetki.keys():
                sessionStorage[user_id]['action'] = False
                sessionStorage[user_id]['danetka'] = req['request']['original_utterance']
                res['response']['text'] = Danetki[req['request']['original_utterance']]['question']
                return

            else:
                res['response']['text'] = 'Повторите название данетки'

        if sessionStorage[user_id]['danetka']:
            pass



# def say_rules1(req, res):
#     if yes_or_no(req):
#         res['response']['text'] = 'Хорошо! Тогда давай играть, выбери Данетку:'
#     else:
#         res['response']['text'] = rules + 'Давай играть?'
#     return
#
#
# def say_rules2(req, res):
#     if yes_or_no(req):
#         res['response']['text'] = str([e for e in Danetki.keys()])[2:-2]
#     else:
#         res['response']['text'] = 'Очень жаль...'


def get_first_name(req):
    # Перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # Находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Иначе возвращаем None.
            return entity['value'].get('first_name', None)


def yes_or_no(req, res):
    or_ut = natasha(req['request']['original_utterance']).lower()
    for y in Yes:
        if y in or_ut:
            return True
    for n in No:
        if n in or_ut:
            return False
    res['response']['text'] = 'Повтори, пожалуйста. Я не поняла твой ответ. Скажи "Да" или "Нет"'
    return
    # Функция вернёт True, если ответ положительный
    # и вернёт False, если ответ отрицательный


def natasha(text):
    text = text.replace(".", "")
    text = text.replace("!", "")
    text = text.replace("?", "")
    text = text.replace("-", "")
    text = text.replace(",", "")
    text = text.replace(":", "")
    text = text.replace(";", "")
    # Избавляемся от всех знаков во входящем
    # тексте для дальнейшей обработки
    return text


if __name__ == '__main__':
    app.run()
