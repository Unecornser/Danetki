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
            'game': None,
            'for_hints': {
                'Удивительный парашютист': {
                    'где находится самолет': [
                        ['самолет был на земле', 'самолет стоял на земле', 'самолет уже приземлился',
                         'самолет еще не взлетал', 'самолет приземлился', 'самолет стоял на взлетной полосе',
                         'Самолет находился на взлетной полосе',
                         'самолет не летел', 'самолет стоял'], False, False],
                },
                'Девушка в автобусе': {
                    'возраст кати играет роль': [
                        ['девочка ребенок', 'девочка маленькая', 'катя ребенок', 'катя очень маленькая',
                         'катя была ребенок', 'она была ребенком', 'катя была ребенком'], False, False
                    ],
                    'место на котором сидит катя': [
                        ['девочка на коленках', 'катя на коленках', 'катя сидела у кого то на коленях',
                         'колени это место''она сидела у кого то на коленях', ], False, False
                    ],
                    'проблема в месте': [
                        ['девочка была не на сиденье', 'девочка сидела не на сиденье', 'катя сидела на ком то',
                         'катя сидела на чем то', 'девочка сидела на чем то', 'под катей что то было'], False, False
                    ],
                    'катя с кем то': [
                        ['девочка была с кем то из родителей', 'катя была с мужчиной', 'папа был с катей',
                         'девочка его дочь', 'катя была с кем то из родителей', 'катя с папой', 'этот мужчина ее отец',
                         'она с кем то', 'у кати есть папа', 'этот мужчина отец', 'папа был с ребенком',
                         'это был папа кати', 'папа был с катей', 'она ехала с батей', 'мужик папа', 'колени это место',
                         'она сидела на коленях у родственника', 'девочка на коленках', 'катя дочь мужчины',
                         'катя была с кем то из родителей', 'он папа'
                         ], False, False
                    ],
                },
                'Фрэнк и приступ': {
                    'какая у фрэнка работа': [
                        ['фрэнк актер', 'фрэнк был актер', 'френк рабоатет в театре', 'фрэнк работал в театре',
                         'его работа в театре', 'он актер', 'он был актер', 'фрэнк был актером', 'он был актером',
                         'он артист', 'фрэнк артист'], False, False
                    ]
                },
                'Загадочный человек': {
                    'у него необычный рост': [
                        ['это связано с ростом', 'это связано с его ростом', 'это из за роста',
                         'из за роста', 'рост был причиной', 'он был маленький', 'он низкий',
                         'ответ как то связан его ростом',
                         'его рост имеет значение', 'рост этого человека имеет значение', 'это было связано с ростом',
                         'он был ниже чем другие люди', 'он отличался ростом от других людей',
                         'он отличался от других детей ростом', 'он был намного ниже людей своего возраста',
                         'этот человек был намного ниже людей своего возраста', 'он карлик', 'он карликового роста',
                         'он слишком маленький', 'он не дотягивается'], False, False
                    ],
                    'он не может нажать': [
                        ['второй он нужен для кнопки 9',
                         'когда он с кем то он едет до конца', 'у него были свои особенности', 'он был особенным',
                         'он особенный человек', 'он особенный', 'он физически не может',
                         'он не может нажать на кнопку',
                         'он может поехать до своего этажа на лифте только если в нем есть кто то еще',
                         'он может поехать до 9 этажа если едет в лифте с кемто', 'он не может нажать',
                         'ему помогал нажать кнопку выше человек который ехал с ним в лифте',
                         'ему помогали нажимать кнопку 9 этажа', 'ему помогали нажать на кнопку выше 7 этажа'], False,
                        False
                    ],
                    'дело в самом человеке': [
                        ['он необычный', 'это из за человека', 'это связано с человеком', 'человек связан с этим',
                         'этому есть причина', 'этому была причина', 'он не дотягивался', 'он не мог доехать',
                         'он не мог нажать', 'не мог доехать', 'он не может нажать кнопку 9 когда едет 1',
                         '1 не может до 9', 'это зависит от его физических возможностей', 'у него больное тело',
                         'у него есть деффекты', 'он был особенным', 'дело в этом человеке', 'человек необычный',
                         'это как то связано с человеком'],
                        False, False
                    ]
                },
                'Безносая смерть': {
                    'То, что прошло 3 месяца - важно': [
                        {'3 месяца сязанны с зимой', '3 месяца это время года', '3 месяца важно',
                         'важно ли именно 3 месяца', 'важно именно 3 месяца', 'время имеет значение',
                         'на именно 3 месяца необходимо обращать внимание', 'важно ли что именно 3 месяца',
                         '3 месяца это какое то время года', '3 месяца связаны с временами года', '3 месяца это важно',
                         '3 месяца  это определённый период', '3 месяца это зима', 'именно 3 месяца это важно'
                         'на 3 месяца необходимо обращать внимание', 'важно что именно 3 месяца',
                         'на 3 месяца нужно обращать вниманиена именно 3 месяца нужно обращать внимание',
                         '3 месяца это одно время года3 месяца это время года', '3 месяца связанны свременем года',
                         'именно 3 месяца важно', 'важно ли то что он умер через 3 месяца'},
                        False, False
                    ],
                    'он не живое сущесво': [
                        {'он неживой', 'это предмет неживой', 'оно неодушевленное', 'это неодушевленное',
                         'этот предмет неодушевленный', 'он неодушевленный', 'это неживое',
                         'это предмет не живое существо', 'это неживой'
                         'оно неживое', 'оно не живое существо', 'это неживое существо', 'он неживое сущесnво'},
                        False, False
                    ],
                    'он умер весной': [
                        {'этого не стало весно', 'это умерло весной', 'его не стало весной', 'не стало этого весной',
                         'не стало его как только наступила весна', 'этот предмет здох весной', 'он умер весной',
                         'он здох весной', 'оно умело весной', 'не стало этого как только наступила весна',
                         'этого предмета не стало весной', 'оно здохло весной', 'не стало этого предмета весной',
                         'этот предмет умер весной', 'не стало его весной'},
                        False, False
                    ],
                    'он бывает только зимой': [
                        {'этот предмет существует только зимой', 'он бывает только зимой', 'он бывает только в зиму',
                         'этот предмет может быть только зимой', 'этот предмет бывает только зимой',
                         'это бывает только зимой', 'он существует только зимой', 'эта ситуация бывает только зимой',
                         'он только зимой', 'этот предмет только зимой', 'он может быть только в зиму',
                         'это только зимняя ситуация', 'оно может быть только в зиму', 'это бывает только в зиму',
                         'это предмет бывает только в зиму', 'он может быть только зимой', 'это существует только зимой',
                         'это может быть только зимой', 'оно существует только зимой', 'эта ситуация только зимой',
                         'эта ситуация может быть только в зиму', 'оно бывает только зимой', 'это только зимой',
                         'это может быть только в зиму', 'оно только зимой', 'оно бывает только в зиму',
                         'оно может быть только зимой', 'только в зиму это может быть',
                         'этот предмет может быть только в зиму'},
                        False, False
                    ],
                    'он сделан из снега': [
                        {'этот предмет сделан из снега', 'этот предмет что то сделанное из снега', 'он из снега',
                         'он что то сделанное из снега', 'это что то из снега', 'это что то сделанное из снега',
                         'оно что то связанное с снегом', 'этот предмет снежный', 'это из снега',
                         'это что то сделанное из снега', 'этот предмет что то связанное с снегом',
                         'это снежное', 'это что то связанное с снегом', 'этот предмет связан с снегом',
                         'он снежный', 'он связан с снегом', 'он что то  связанное с снегом', 'это сделанное из снега',
                         'это связано с снегом', 'оно сделано из снега', 'он из снега сделан',
                         'этот предмет что то из снега', 'оно сделанное из снега', 'оно снежное', 'он сделан из снега',
                         'он сделан из снега',  'это предмет что то из снега', 'из снега', 'оно из снега',
                         'это сделано из снега', 'оно что то сделанное из снега', 'оно связано с снегом'},
                    False, False
                    ]
                }
            }
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

                    res['response']['text'] = rules_txt + 'Теперь выбери Данету:\n' + Dan_keys_txt
                elif yes_or_no(req, res, user_id, sessionStorage[user_id]['action'], 'Ты знаешь правила игры?') == 'ya':
                    return

                else:
                    res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому"' \
                                              '\n\nТы знаешь правила игры?'
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

                elif yes_or_no(req, res, user_id, None, 'Ты знаешь правила игры?') == 'ya':
                    return

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
                    elif select(req, res, user_id) == 'ya':
                        return
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
                elif yes_or_no(req, res, user_id, 'end_Dan', 'Хотите ещё Данетку?') is False:
                    res['response']['text'] = 'Приятно было поиграть, пока-пока'
                    res['response']['end_session'] = True
                else:
                    res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому или, если что-то ' \
                                              'не так, скажи "Помощь"\n\nХотите ещё Данетку?'
        return


def game_mode(req, res, user_id):
    # Функция узнаёт и передёт в sessionStorage[user_id]['game_mode']
    # режим игры (однопользовательский или многопользовательский).

    or_ut = req['request']['original_utterance'].lower().replace('ё', 'е')
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

    or_ut = req['request']['original_utterance'].lower().replace('ё', 'е')
    for key in Danetki.keys():
        if or_ut in key.lower():
            res['response']['text'] = random.choice(['Отлично! ', 'Хороший выбор! ']) + Danetki[key]['question']
            return key

    if check_another_oper(req, res, user_id, 'select_mode', select_txt) is True:
        return 'ya'
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
    or_ut = req['request']['original_utterance'].lower().replace('ё', 'е')

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
        return
    elif check_another_oper(req, res, user_id, action, text) is True:
        return 'ya'


def txt_nat(text):
    text = text.replace("наверное", "")
    text = text.replace("я считаю что", "")
    text = text.replace("я считаю", "")
    text = text.replace("может быть", "")
    text = text.replace("возможно", "")
    text = text.replace("типа", "")
    text = text.replace("вообще", "")
    text = text.replace("ё", "е")

    # Избавляемся от лишнего в
    # тексте для дальнейшей обработки.

    return text


###############################
# Функции из standart_functions
###############################


def check_another_oper(req, res, user_id, action, text):
    # Функция проверяет, вызывал ли пользователь
    # что-либо из standart_functions

    or_ut = req['request']['original_utterance'].lower().replace('ё', 'е')
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
    for word in Wt_i_kn_list:  # Повтор вопросов пользователя с ответом "да"
        if word in or_ut:
            ret = 5
    for word in Hint_list:  # Подсказка
        if word in or_ut:
            ret = 6
    for word in Rules_list:  # Правила
        if word in or_ut:
            ret = 7
    for word in Continue_list:  # Продолжить играть
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
        what_i_know(res, user_id)
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


def what_i_know(res, user_id):
    Hints = sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']]

    res['response']['text'] = 'Ты уже знаешь такие детали:\n'
    for hint in Hints:
        if Hints[hint][1] is True:
            res['response']['text'] += hint
    if res['response']['text'][-2] == ':':
        res['response']['text'] = 'Пока что ты не узнал ничего особенного об этой Данетке.'
    return


def hint(res, user_id):
    Hints = sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']]
    for hint in Hints:
        if Hints[hint][1] is False:
            sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']][hint][2] = True
            res['response']['text'] = hint
            return
    res['response']['text'] = 'Прости, подсказки закончились. Попробуй по-другому формулировать свои ' \
                              'вопросы и у тебя всё получится'
    return


def play(req, res, user_id):
    answer = Alice_anwer(req, res)

    if answer == 1:
        res['response']['text'] = random.choice(['Да', 'Верно!', 'Ага', 'Угу'])
    elif answer == 2:
        res['response']['text'] = random.choice(['Не', 'Неа', 'А вот и нет', 'Нет'])
    elif answer == 3:
        single_final2(res, req, user_id)
    elif answer == 4:
        return
    elif answer == 5:
        res['response']['text'] = random.choice(['Не имеет значения', 'Это неважно'])
    if single_final1(user_id) is True:
        res['response']['text'] = 'Кажется, ты уже знаешь всё о Данетке. Попробуй сказать весь ответ полностью, ' \
                                  'если не получается - скажи: "Алиса, что я уже знаю?"'
        sessionStorage[user_id]['action'] = 'final'
    return


def Alice_anwer(req, res):
    user_id = req['session']['user_id']
    danetka = sessionStorage[user_id]['game']
    Hints = sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']]
    or_ut = ' '.join(sorted(txt_nat(req['request']['original_utterance']).lower().split()))

    if or_ut in Danetki[danetka]['answers']:
        return 3
    elif or_ut in Danetki[danetka]['yes']:
        for hint in Hints:
            if or_ut in Hints[hint][0]:
                sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']][hint][1] = True
                sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']][hint][2] = True
        return 1
    elif or_ut in Danetki[danetka]['no']:
        return 2
    elif check_another_oper(req, res, user_id, 'play', 'Отлично, продолжай разгадывать Данетку') is True:
        return 4
    else:
        return 5


def wait_user_answer(req, res, user_id, action, text):
    user_answer = req['request']['original_utterance'].lower().replace('ё', 'е')

    for word in Multi_complete_list:
        if word in user_answer:
            return 1
    if check_another_oper(req, res, user_id, action, text) is True:
        return
    else:
        res['response']['text'] = 'Прости, я не поняла твой ответ. Скажите, когда вы разгадаете ' \
                                  'Данетку или, если что-то не так, скажите "Помощь"'
        return


def single_final1(user_id):
    Hints = sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']]

    for hint in Hints:
        if Hints[hint][1] is False:
            return False
    else:
        return True


def single_final2(res, req, user_id):
    or_ut = req['request']['original_utterance'].lower().replace('ё', 'е')
    Answers = Danetki[sessionStorage[user_id]['game']]['answers']

    if or_ut in Answers:
        res['response']['text'] = 'Да! Именно! Если хочешь ещё Данетку, скажи: "Алиса, я хочу другую Данетку".'
        return
    elif check_another_oper(req, res, user_id, 'final',
                            'Ты очень близко к разгадке тайны. Дай полный ответ на Данетку'):
        return
    res['response']['text'] = 'Нет'
    return


if __name__ == '__main__':
    app.run()
