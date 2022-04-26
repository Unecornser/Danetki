from flask import Flask, request
from texts import *
from keys import *
import logging
import json
import random
# from standart_functions import *
# from single import *
# from multi import *


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
                                      '! Я - Алиса. Ты знаешь правила игры?'

    else:
        if sessionStorage[user_id]['action'] is None:

            # Если поле sessionStorage[user_id]['action'] пустое,
            # значит на данный момент пользователь либо не начал,
            # либо только что закончил отгадывать Данетку.

            if yes_or_no(req, res, user_id, sessionStorage[user_id]['action'], 'Ты знаешь правила игры?') is True:
                res['response']['text'] = 'Хорошо! Выбери режим игры:\n\nИграть самому\nИграть с друзьями'
            elif yes_or_no(req, res, user_id, sessionStorage[user_id]['action'], 'Ты знаешь правила игры?') is False:
                res['response']['text'] = rules_txt + '\n\n' + ' Выбери режим игры:\n\nИграть самому\nИграть с друзьями'
            else:
                res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому или, если что-то ' \
                                              'не так, скажи "Помощь"\n\nТы знаешь правила игры?'
                return
            sessionStorage[user_id]['action'] = 'select_mode'

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

                    text = Danetki[sessionStorage[user_id]['game']]['question']
                    answer = Danetki[sessionStorage[user_id]['game']]['answer']

                    if sessionStorage[user_id]['game_mode'] == 'multi_player':
                        res['response']['text'] = multi_rules_txt + '\n\nА теперь Данетка\n\n' + \
                                                  text + '\n\n\nОтвет:\n' + answer
                    else:
                        res['response']['text'] = text
                    sessionStorage[user_id]['action'] = 'play'

        elif sessionStorage[user_id]['action'] == 'play':

            # Начинается игра. Алиса читает условие Данетки.

            if sessionStorage[user_id]['game_mode'] == 'single_player':
                play(req, res, sessionStorage)
            elif sessionStorage[user_id]['game_mode'] == 'multi_player':
                print('Multiplayer zone')
                if wait_user_answer(req, res, user_id, 'play', 'Продолжайте разгадывать Данетку') == 1:
                    res['response']['text'] = 'Отлично! Вы молодцы. Хотите ещё Данетку?'
    return


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
                                      Dan_keys_txt
            return 'single_player'
    for multi in multi_player:
        if multi in or_ut:
            res['response']['text'] = random.choice(['Отлично!', 'Хорошо!', 'Поняла,']) + ' Теперь выбери Данетку\n' + \
                                      Dan_keys_txt
            return 'multi_player'
    if check_another_oper(req, res, user_id, 'select_mode', game_mode_txt) is False:
        res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому'
    return
    # Функция вернёт True, если ответ положительный
    # и вернёт False, если ответ отрицательный


def select(req, res, user_id):
    # Функция узнаёт и передаёт в sessionStorage[user_id]['action']
    # ту Данетку, которую выбрал пользователь.

    or_ut = natasha(req['request']['original_utterance']).capitalize()
    if or_ut in Danetki.keys():
        res['response']['text'] = random.choice(['Отлично! ', 'Хороший выбор! ']) + Danetki[or_ut]['question']
        return or_ut.capitalize()
    else:
        if check_another_oper(req, res, user_id, 'select_mode', select_txt) is False:
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


def yes_or_no(req, res, user_id, action, text):
    or_ut = natasha(req['request']['original_utterance']).lower()

    # Функция вернёт True, если ответ положительный
    # и вернёт False, если ответ отрицательный
    for y in Yes_list:
        if y in or_ut:
            return True
    for n in No_list:
        if n in or_ut:
            return False
    if check_another_oper(req, res, user_id, sessionStorage[user_id]['action'], text) is False:
        res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи "Да" или "Нет" или, ' \
                              'если что-то не так, скажи "Помощь"'


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


###############################
# Функции из standart_functions
###############################


def check_another_oper(req, res, user_id, action, text):
    # Функция проверяет, вызывал ли пользователь
    # что-либо из standart_functions

    or_ut = natasha(req['request']['original_utterance']).lower()
    ret = 0
    for word in Help_list:  # Помощь
        if word in or_ut:
            ret = 1
    for word in Comm_list:  # Команды
        if word in or_ut:
            ret = 2
    for word in An_Dan_list:  # Другая Данетка
        if word in or_ut:
            ret = 3
    for word in Repeate_list:  # Повторить Данетку
        if word in or_ut:
            ret = 4
    for word in Wt_i_kn_list:  # повтор вопросов пользователя с ответом "да"
        if word in or_ut:
            ret = 5
    for word in Hint_list:  # Подсказка
        if word in or_ut:
            ret = 6
    for word in Rules_list:  # Правила
        if word in or_ut:
            ret = 7
    for word in Continue_list:  # Правила
        if word in or_ut:
            ret = 8
    return use_stand_func(ret, res, user_id, action, text)


def use_stand_func(ret, res, user_id, action, text):
    # Выполняется нужная функция исходя из
    # результатов проверки в check_another_oper()

    if ret == 0:
        return False
    elif ret == 1:
        res['response']['text'] = help_txt
        # Алиса говорит, как можно решить какую-либо проблему (читает help_txt)
    elif ret == 2:
        res['response']['text'] = commands_txt
        # Алиса читает commands_txt
    elif ret == 3:
        sessionStorage[user_id]['action'] = None
        # Другая Данека
    elif ret == 4:
        res['response']['text'] = Danetki[sessionStorage[user_id]['game']]['question']
        # Алиса повторяет условие Данетки
    elif ret == 5:
        res['response']['text'] = 'Эта функция ещё не написана'
        print('Эта функция ещё не написана')
        # what_i_know()
    elif ret == 6:
        res['response']['text'] = 'Эта функция ещё не написана'
        print('Эта функция ещё не написана')
        # hint()
    elif ret == 7:
        res['response']['text'] = rules_txt
        # Алиса повторяет правила игры (читает rules_txt)
    elif ret == 8:
        res['response']['text'] = text
        sessionStorage[user_id]['action'] = action
    return True


'''
def what_i_know(res):


def hint(Hints_array, res):
'''


def play(req, res):
    answer = Alice_anwer(req, res)

    if answer == 1:
        res['response']['text'] = 'Да'
    elif answer == 2:
        res['response']['text'] = 'Нет'
    elif answer == 3:
        res['response']['text'] = 'Не имеет значения'
    return


def Alice_anwer(req, res):
    user_id = req['session']['user_id']
    or_ut = natasha(req['request']['original_utterance']).lower()
    danetka = sessionStorage[user_id]['game']

    if or_ut in Danetki[danetka]['yes']:
        return 1
    elif or_ut in Danetki[danetka]['no']:
        return 2
    elif check_another_oper(req, res, user_id):
        return 3


def wait_user_answer(req, res, user_id, action, text):
    user_answer = natasha(req['request']['original_utterance']).lower()

    for word in Multi_complete_list:
        if word in user_answer:
            return 1
    check_another_oper(req, res, user_id, action, text)


if __name__ == '__main__':
    app.run()
