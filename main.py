from flask import Flask, request
from single import *
from multi import *
from texts import *
from standart_functions import *
import logging
import json
import random


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
        res['response']['text'] = 'Привет, давай поиграем в Данетки! Как тебя зовут?'
        # создаем словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'first_name': None,
            'action': None,
            'game_mode': None,
            'game': None
        }
        return

    # Если пользователь не новый, то попадаем сюда.
    # Если поле имени пустое, то это говорит о том,
    # что пользователь еще не представился.
    if sessionStorage[user_id]['first_name'] is None:
        # В последнем его сообщение ищем имя.
        first_name = get_first_name(req, res, user_id)
        # Если не нашли, то сообщаем пользователю, что не расслышали.
        if first_name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        # Если нашли, то приветствуем пользователя
        # и спрашиваем знает ли он правила.
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response']['text'] = 'Здравствуй, ' + first_name.title() + \
                                      '! Я - Алиса. Тызнаешь правила игры?'
            return
    else:
        if sessionStorage[user_id]['action'] is None:

            # Если поле sessionStorage[user_id]['action'] пустое,
            # значит на данный момент пользователь либо не начал,
            # либо только что закончил отгадывать Данетку.

            if yes_or_no(req, res, user_id):
                res['response']['text'] = 'Хорошо! Выбери режим игры:\n\nИграть самому\nИграть с друзьями'
            else:
                res['response']['text'] = rules + '\n\n' + ' Выбери режим игры:\n\nИграть самому\nИграть с друзьями'
            sessionStorage[user_id]['action'] = 'select_mode'
            return

        elif sessionStorage[user_id]['action'] == 'select_mode':  # Выбор режима игры
            if sessionStorage[user_id]['game_mode'] is None:
                sessionStorage[user_id]['game_mode'] = game_mode(req, res, user_id)
            else:

                # Блок выбора Данетки.
                # Пользователь называет выбранную Данетку

                sessionStorage[user_id]['game'] = select(req, res, user_id)
                if sessionStorage[user_id]['game'] is None:
                    res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому или, если что-то ' \
                                              'не так, скажи "Помощь"'

                else:  # Функция вернула название Данетки => продолжаем

                    text = Danetki[sessionStorage[user_id]['game'].capitalize()][0]
                    answer = Danetki[sessionStorage[user_id]['game'].capitalize()][1]

                    if sessionStorage[user_id]['game_mode'] == 'multi_player':
                        res['response']['text'] = multi_rules + '\n\nА теперь Данетка\n\n' + \
                                                  text + '\n\n\nОтвет:\n' + answer
                    else:
                        res['response']['text'] = text
                    sessionStorage[user_id]['action'] = 'play'
                    return
        elif sessionStorage[user_id]['action'] == 'play':

            # Начинается игра. Алиса читает условие Данетки.

            if sessionStorage[user_id]['game_mode'] == 'single_player':
                play(req, res, sessionStorage)
            elif sessionStorage[user_id]['game_mode'] == 'multi_player':
                print('-_-')
                # if wait_user_answer(req) == 1:
                #     res['response']['text'] = 'Отлично! Вы молодцы. Хотите ещё Данетку?'


def game_mode(req, res, user_id):
    # Функция узнаёт и передёт в sessionStorage[user_id]['game_mode']
    # режим игры (однопользовательский или многопользовательский).

    single_player = ['один', 'сам', 'сингл', 'в соло', 'всоло', 'в солянова', 'всоланова', 'в одиночку', 'по одному',
                     'собственными силами', 'без поддержки', 'одельно', 'поодиночке', 'порознь', 'в гордом одиночестве',
                     'врознь', 'поврозь', 'розно']
    multi_player = ['вместе', 'бок о бок', 'за компанию', 'одновременно', 'не один', 'не одна', 'много', 'совместно',
                    'плечом к плечу', 'вдвоем', 'втроем', 'вчетвером', 'впятером', 'вшестером', 'всемером', 'заодно',
                    'все', 'воедино', 'вкупе', 'сообща', 'единодушно', 'хором', 'коллективно', 'в тандеме',
                    'в сборе', 'заедино', 'воедино', 'мульт', 'друг', 'друз', 'друж']

    or_ut = natasha(req['request']['original_utterance']).lower()
    for single in single_player:
        if single in or_ut:
            res['response']['text'] = random.choice(['Отлично!', 'Хорошо!', 'Поняла,']) + ' Теперь выбери Данетку\n' + \
                                      Dan_keys
            return 'single_player'
    for multi in multi_player:
        if multi in or_ut:
            res['response']['text'] = random.choice(['Отлично!', 'Хорошо!', 'Поняла,']) + ' Теперь выбери Данетку\n' + \
                                      Dan_keys
            return 'multi_player'

    res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому'
    return
    # Функция вернёт True, если ответ положительный
    # и вернёт False, если ответ отрицательный


def select(req, res, user_id):
    # Функция узнаёт и передаёт в sessionStorage[user_id]['action']
    # ту Данетку, которую выбрал пользователь.

    or_ut = natasha(req['request']['original_utterance']).lower()
    if or_ut in Danetki.keys():
        res['response']['text'] = random.choice(['Отлично! ', 'Хороший выбор! ']) + Danetki[or_ut]['question']
        return or_ut
    else:
        if check_another_oper(req, res, user_id) is False:
            # Если пользователь сказал что-то невнятно, либо
            # выбрал несуществующую историю, Алиса переспросит.
            res['response']['text'] = 'Я не знаю такую Данетку. Скажи ещё раз.'
            return None
        return


def get_first_name(req, res, user_id):
    # Перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # Находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Иначе возвращаем None.
            return entity['value'].get('first_name', None)
    check_another_oper(req, res, user_id)


def yes_or_no(req, res, user_id):
    or_ut = natasha(req['request']['original_utterance']).lower()
    for y in Yes:
        if y in or_ut:
            return True
    for n in No:
        if n in or_ut:
            return False
    if check_another_oper(req, res, user_id) is False:
        res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи "Да" или "Нет" или, ' \
                              'если что-то не так, скажи "Помощь"'
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
    text = text.replace("ё", "е")
    # Избавляемся от всех знаков во входящем
    # тексте для дальнейшей обработки.
    # Также меняем "ё" на "е"
    return text


if __name__ == '__main__':
    app.run()
