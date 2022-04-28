from flask import Flask, request
from texts import *
from keys import *
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

    if req['session']['new']:

        res['response']['text'] = 'Привет, давай играть в Данетки! Ты знаешь правила игры?'
        # создаем словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'action': None,
            'game_mode': None,
            'game': None
        }
        if 'Linux' in req['meta']['client_id']:
            sessionStorage['OS'] = 'Yandex'
        else:
            sessionStorage['OS'] = 'display'
        return

    else:
        if sessionStorage['OS'] == 'Yandex':
            if sessionStorage[user_id]['action'] is None:

                # Если поле sessionStorage[user_id]['action'] пустое,
                # значит на данный момент пользователь либо не начал,
                # либо только что закончил отгадывать Данетку.

                if yes_or_no(req, res, user_id, sessionStorage[user_id]['action'], 'Ты знаешь правила игры?') is True:
                    res['response']['text'] = 'Хорошо! Выбери Данетку:\n' + Dan_keys_txt

                elif yes_or_no(req, res, user_id, sessionStorage[user_id]['action'],
                               'Ты знаешь правила игры?') is False:
                    res['response']['text'] = rules_txt
                else:
                    res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому или, если что-то ' \
                                              'не так, скажи "Помощь"\n\nТы знаешь правила игры?'
                    return
                sessionStorage[user_id]['action'] = 'select_mode'

            elif sessionStorage[user_id]['action'] == 'select_mode':

                # Блок выбора Данетки.
                # Пользователь называет выбранную Данетку

                sessionStorage[user_id]['game'] = select(req, res, user_id)
                if sessionStorage[user_id]['game'] is None:
                    res['response']['text'] = 'Я не знаю такую Данетку, скажи ещё раз\n' + Dan_keys_txt
                else:  # Функция вернула название Данетки => продолжаем

                    text = Danetki[sessionStorage[user_id]['game']]['question']

                    res['response']['text'] = text
                    sessionStorage[user_id]['action'] = 'play'

            elif sessionStorage[user_id]['action'] == 'play':
                # Начинается игра. Алиса читает условие Данетки.
                play(req, res, user_id)

            elif sessionStorage[user_id]['action'] == 'final':
                single_final2(res, req, user_id)
                return

        elif sessionStorage['OS'] == 'display':
            if sessionStorage[user_id]['action'] is None:

                # Если поле sessionStorage[user_id]['action'] пустое,
                # значит на данный момент пользователь либо не начал,
                # либо только что закончил отгадывать Данетку.

                if yes_or_no(req, res, user_id, None, 'Ты знаешь правила игры?') is True:
                    res['response']['text'] = 'Хорошо! Выбери режим игры:\n\nИграть с Алисой\nИграть с друзьями'
                    res['response']['tts'] = 'Хорошо! Выбери режим игры:\n\nИграть с Алисой или Играть с друзьями'

                elif yes_or_no(req, res, user_id, None, 'Ты знаешь правила игры?') is False:
                    res['response']['text'] = rules_txt + '\n\n' + \
                                              'Выбери режим игры:\n\nИграть с Алисой\nИграть с друзьями'

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
                        res['response']['text'] = 'Я не знаю такую Данетку, скажи ещё раз\n' + Dan_keys_txt
                    else:  # Функция вернула название Данетки => продолжаем

                        text = Danetki[sessionStorage[user_id]['game']]['question']
                        if sessionStorage[user_id]['game_mode'] == 'multi_player':
                            image = Danetki[sessionStorage[user_id]['game']]['image']
                            description = text + '\n\n\nОтвет на фотографии\n'

                        if sessionStorage[user_id]['game_mode'] == 'multi_player':
                            res['response']['card'] = dict()
                            res['response']['card']['type'] = 'BigImage'
                            res['response']['card']['image_id'] = image
                            res['response']['card']['description'] = description
                        else:
                            res['response']['text'] = text
                        sessionStorage[user_id]['action'] = 'play'

            elif sessionStorage[user_id]['action'] == 'play':

                # Начинается игра. Алиса читает условие Данетки.

                if sessionStorage[user_id]['game_mode'] == 'single_player':
                    play(req, res, user_id)
                elif sessionStorage[user_id]['game_mode'] == 'multi_player':
                    print('Multiplayer zone')
                    if wait_user_answer(req, res, user_id, 'play', 'Продолжайте разгадывать Данетку') == 1:
                        res['response']['text'] = 'Отлично! Вы молодцы. Хотите ещё Данетку?'
                        sessionStorage[user_id]['action'] = 'end_Dan'

            elif sessionStorage[user_id]['action'] == 'final':
                single_final2(res, req, user_id)
                return

            elif sessionStorage[user_id]['action'] == 'end_Dan':
                if yes_or_no(req, res, user_id, 'end_Dan', 'Хотите ещё Данетку?') is True:
                    res['response']['text'] = 'Хорошо, секунду. Вы помните правила?'
                    sessionStorage[user_id]['action'] = None
                    sessionStorage[user_id]['game_mode'] = None
                    sessionStorage[user_id]['game'] = None
                else:
                    res['response']['text'] = 'Приятно было поиграть, пока-пока'
                    res['response']['end_session'] = True
        return


def game_mode(req, res, user_id):
    # Функция узнаёт и передёт в sessionStorage[user_id]['game_mode']
    # режим игры (однопользовательский или многопользовательский).

    or_ut = natasha(req['request']['command']).lower()
    for single in single_player_list:
        if single in or_ut:
            res['response']['text'] = random.choice(['Отлично!', 'Хорошо!', 'Поняла,']) + \
                                      ' Теперь выбери Данетку:\n' + Dan_keys_txt
            return 'single_player'
    for multi in multi_player_list:
        if multi in or_ut:
            res['response']['text'] = multi_rules_txt + '\n\n' + random.choice(['Отлично!', 'Хорошо!', 'Поняла,']) + \
                                      ' Теперь выберите Данетку:\n' + Dan_keys_txt
            return 'multi_player'

    if check_another_oper(req, res, user_id, 'select_mode', game_mode_txt) is False:
        res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому'
    return
    # Функция вернёт True, если ответ положительный
    # и вернёт False, если ответ отрицательный


def select(req, res, user_id):
    # Функция узнаёт и передаёт в sessionStorage[user_id]['game']
    # ту Данетку, которую выбрал пользователь.

    or_ut = natasha(req['request']['command']).lower()
    for key in Danetki.keys():
        if or_ut in key.lower():
            res['response']['text'] = random.choice(['Отлично! ', 'Хороший выбор! ']) + Danetki[key]['question']
            return key

    if check_another_oper(req, res, user_id, 'select_mode', select_txt) is False:
        # Если пользователь сказал что-то невнятно, либо
        # выбрал несуществующую историю, Алиса переспросит.
        res['response']['text'] = 'Я не знаю такую Данетку. Скажи ещё раз.'
        return
    return None


def get_first_name(req):
    # Перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # Находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Иначе возвращаем None.
            return entity['value'].get('first_name', None)


def yes_or_no(req, res, user_id, action, text):
    or_ut = natasha(req['request']['command']).lower()

    # Функция вернёт True, если ответ положительный
    # и вернёт False, если ответ отрицательный
    for y in Yes_list:
        if y in or_ut:
            return True
    for n in No_list:
        if n in or_ut:
            return False
    if check_another_oper(req, res, user_id, action, text) is False:
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
    text = text.replace("наверное", "")
    text = text.replace("я считаю что", "")
    text = text.replace("я считаю", "")
    text = text.replace("как то", "")
    text = text.replace("что то", "")
    text = text.replace("зачем то", "")
    text = text.replace("почему то", "")
    text = text.replace("вообще то", "")
    text = text.replace("ведь", "")
    text = text.replace("человек", "он")
    text = text.replace("женщина", "девушка")
    text = text.replace("может быть", "")
    text = text.replace("возможно", "")
    text = text.replace("косвенно", "")
    text = text.replace("типа", "")
    text = text.replace("типо", "")
    text = text.replace("вообще", "")
    text = text.replace("была", "")
    text = text.replace("был", "")

    # Избавляемся от лишнего в
    # тексте для дальнейшей обработки.

    return text


###############################
# Функции из standart_functions
###############################


def check_another_oper(req, res, user_id, action, text):
    # Функция проверяет, вызывал ли пользователь
    # что-либо из standart_functions

    or_ut = natasha(req['request']['command']).lower()
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
        res['response']['text'] = 'Хорошо, секунду. Ты помнишь правила?'
        sessionStorage[user_id]['action'] = None
        sessionStorage[user_id]['game_mode'] = None
        sessionStorage[user_id]['game'] = None
        # Другая Данека
    elif ret == 4:
        try:
            res['response']['text'] = Danetki[sessionStorage[user_id]['game']]['question']
        except:
            pass
        # Алиса повторяет условие Данетки
    elif ret == 5:
        res['response']['text'] = 'Эта функция ещё не написана'
        print('Эта функция ещё не написана')
        # what_i_know()
    elif ret == 6:
        # res['response']['text'] = 'Эта функция ещё не написана'
        # print('Эта функция ещё не написана')
        hint(res, user_id)
    elif ret == 7:
        res['response']['text'] = rules_txt
        # Алиса повторяет правила игры (читает rules_txt)
    elif ret == 8:
        res['response']['text'] = text
        sessionStorage[user_id]['action'] = action
    return True


# def what_i_know(res):


def hint(res, user_id):
    Hints = Danetki[sessionStorage[user_id]['game']]['hints']
    for hint in Hints:
        if Hints[hint][1] is False:
            Danetki[sessionStorage[user_id]['game']]['hints'][hint][1] = True
            res['response']['text'] = hint
            return
    res['response']['text'] = 'Прости, подсказки закончились. Попробуй по-другому формулировать свои ' \
                              'вопросы и у тебя всё получится'
    return


def play(req, res, user_id):
    answer = Alice_anwer(req, res)

    if answer == 1:
        res['response']['text'] = random.choice(['Да', 'Верно!', 'Ага', "Угу"])
    elif answer == 2:
        res['response']['text'] = random.choice(['Не', 'Неа', 'Мимо', "А вот и нет", "Нет"])
    elif answer == 3:
        single_final2(res, req, user_id)
    elif answer == 4:
        return
    elif answer == 5:
        res['response']['text'] = random.choice(['Не имеет значения', 'Неважно', 'Значения не имеет'])
    if single_final1(user_id) is True:
        res['response']['text'] = 'Кажется, ты уже знаешь всё о Данетке. Попробуй сказать весь ответ полностью, ' \
                                   'если не получается - скажи: "Алиса, что я уже знаю?"'
        sessionStorage[user_id]['action'] = 'final'
    return


def Alice_anwer(req, res):
    user_id = req['session']['user_id']
    or_ut = natasha(req['request']['command']).lower()
    danetka = sessionStorage[user_id]['game']
    Hints = Danetki[sessionStorage[user_id]['game']]['hints']

    for guess in Danetki[danetka]['yes']:
        if or_ut == guess:
            for hint in Hints:
                if guess in Hints[hint][0]:
                    Danetki[sessionStorage[user_id]['game']]['hints'][hint][2] = True
                    Danetki[sessionStorage[user_id]['game']]['hints'][hint][1] = True
            return 1
    for guess in Danetki[danetka]['no']:
        if or_ut == guess:
            return 2
    if or_ut in Danetki[danetka]['answers']:
        return 3
    if check_another_oper(req, res, user_id, 'play', 'Отлично, продолжай разгадывать Данетку') is True:
        return 4
    return 5


def wait_user_answer(req, res, user_id, action, text):
    user_answer = natasha(req['request']['command']).lower()

    for word in Multi_complete_list:
        if word in user_answer:
            return 1
    check_another_oper(req, res, user_id, action, text)


def single_final1(user_id):
    danetka = sessionStorage[user_id]['game']

    for hint in Danetki[danetka]['hints']:
        if Danetki[danetka]['hints'][hint][2]:
            return True
    return False


def single_final2(res, req, user_id):
    or_ut = natasha(req['request']['command']).lower()
    Answers = Danetki[sessionStorage[user_id]['game']]['answers']

    if or_ut in Answers:
        res['response']['text'] = 'Да! Именно! Если хочешь ещё Данетку, скажи: "Алиса, я хочу другую Данетку".'
        return
    elif check_another_oper(req, res, user_id, 'final', 'Ты очень близко к разгадке тайны. Дай полный ответ на Данетку'):
        return
    res['response']['text'] = 'Нет'
    return


if __name__ == '__main__':
    app.run()
