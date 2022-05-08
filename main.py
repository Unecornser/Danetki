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

        res['response']['text'] = 'Привет, давай играть в Данетки! Это увлекательная игра, где тебе нужно угадывать ' \
                                  'предистории, которым последовала необычная ситуация. Ты знаешь правила игры?'

        # создаем словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'action': None,
            'game_mode': None,
            'game': None,
            'for_hints': {
                'Удивительный парашютист': {
                    'где находится самолет': [
                        ['был земле на самолет', 'земле на самолет стоял', 'приземлился самолет уже',
                         'взлетал еще не самолет', 'приземлился самолет', 'взлетной на полосе самолет стоял',
                         'взлетной на находился полосе самолет', 'летел не самолет', 'самолет стоял'], False, False],
                },
                'Девушка в автобусе': {
                    'возраст кати играет роль': [
                        ['девочка ребенок', 'девочка маленькая', 'катя ребенок', 'катя маленькая очень',
                         'была катя ребенок', 'была она ребенком', 'была катя ребенком'], False, False
                    ],
                    'проблема в месте': [
                        ['была девочка на не сиденье', 'девочка на не сидела сиденье', 'катя ком на сидела то',
                         'катя на сидела то чем', 'девочка на сидела то чем', 'было катей под то что',
                         'девочка коленках на', 'катя коленках на', 'катя кого коленях на сидела то у',
                         'колени место это', 'кого коленях на она сидела то у'], False, False
                    ],
                    'катя с кем то': [
                        ['была девочка из кем родителей с то', 'была катя мужчиной с', 'был катей папа с',
                         'девочка дочь его', 'была из катя кем родителей с то', 'катя папой с', 'ее мужчина отец этот',
                         'кем она с то', 'есть кати папа у', 'мужчина отец этот', 'был папа ребенком с',
                         'был кати папа это', 'был катей папа с', 'батей ехала она с', 'мужик папа', 'колени место это',
                         'коленях на она родственника сидела у', 'девочка коленках на', 'дочь катя мужчины',
                         'была из катя кем родителей с то', 'он папа'], False, False
                    ],
                },
                'Загадочный человек': {
                    'дело в самом человеке': [
                        ['необычный он', 'за из человека это', 'с связано человеком это', 'с связан человек этим',
                         'есть причина этому', 'была причина этому', 'дотягивался не он', 'доехать мог не он',
                         'мог нажать не он', 'доехать мог не', '1 9 едет кнопку когда может нажать не он',
                         '1 9 до может не', 'возможностей его зависит от физических это', 'больное него тело у',
                         'деффекты есть него у', 'был он особенным', 'в дело человеке этом', 'необычный человек',
                         'как с связано то человеком это'],
                        False, False
                    ],
                    'у него необычный рост': [
                        {'маленький может он', 'а маленький он', 'за из роста', 'был обычный рост человека этого',
                         'а был маленького роста человек', 'был вероятно карликом он', 'был думаю карликом человек я',
                         'был него обычный рост у', 'был карликом человек', 'а был карликом может человек',
                         'а был может низкого рост человек', 'было ростом с связано это', 'был вероятно маленький он',
                         '170 больше был его рост см', 'был есть маленького меня предположение роста у человек что',
                         'а был маленький он', 'был маленький он', 'карлик он', 'а был низкого рост человек',
                         'был маленького роста человек', 'был маленький он полагаю я', 'был думаю маленький он я',
                         'его ниже рост среднего', 'а маленький может он', 'был низкого рост человек',
                         'маленький он слишком', 'ниже рост среднего человека этого', 'был может низкого рост человек',
                         'был карликом он', 'был другие люди ниже он чем', 'вероятно маленький человек этот',
                         'датентку на ответ ростом с связан человека этого', 'а маленький может человек этот',
                         'был кажется карликом мне он', 'а был низкого рост человек что',
                         'был кажется маленького мне он роста', 'маленького может он роста', 'а маленький он что',
                         'его как ответ ростом связан то', 'был карликом может человек',
                         'был думаю низкого рост человек я', 'был вероятно низкого рост человек',
                         'был возраста людей намного ниже своего человек этот', 'значение имеет рост человека этого',
                         'кажется маленький мне он', 'был кажется мне низкого рост человек', 'а был карликом он что',
                         'был карликом может он', 'был думаю маленького роста человек я', 'дотягивается не он',
                         'его ростом с связано это', 'был кажется маленький мне он', 'а маленький человек этот',
                         'за из роста это', 'был кажется маленького мне роста человек', 'маленький человек этот',
                         'был его маленький очень рост', 'большой него рост у', 'был карлик может он',
                         'его значение имеет рост', 'других людей он от отличался ростом', 'вероятно маленький он',
                         'а был карликом он', 'был возраста людей намного ниже он своего', 'низкий он',
                         'а был маленького может он роста', 'был вероятно маленького он роста',
                         'а был карликом человек что', 'а был маленький может он', 'ростом с связано это',
                         'был думаю маленького он роста я', 'был него обыкновенный рост у',
                         'был маленького полагаю роста человек я', 'маленький он', 'был карликом он полагаю я',
                         'кажется маленький мне человек этот', 'был причиной рост', 'а маленький человек что этот',
                         'а был карликом может он', 'был низкого полагаю рост человек я', 'думаю маленький он я',
                         'был кажется карликом мне человек', 'был думаю карликом он я', 'был маленький может он',
                         'думаю карлик он я', 'карлик может он', 'маленький полагаю человек этот я',
                         'него рост средний у', 'адекватным был человек', 'маленький он полагаю я',
                         'а был маленький он что', 'маленький может человек этот', 'был вероятно карликом человек',
                         'думаю маленький человек этот я', 'был думаю карлик он я', 'был карликом полагаю человек я',
                         'а был карликом человек', 'данетку его на ответ ростом с связан',
                         'девятого до доезжать сам хотел человек этажа', 'был маленького он очень роста',
                         'детей других он от отличался ростом', 'карликового он роста'}, False, False
                    ],
                    'он не может нажать кнопку': [
                        {'до дотянуться кнопки мог он последних этажей', 'была возможность выше до кнопки него у',
                         'кнопку может на нажать не он', 'выше до дотягивался кнопки не он седьмого этажа',
                         'верхних до дотянуться кнопки ли мог он этажей',
                         'а выше до дотягивался кнопки не он седьмого что этажа',
                         'выше до дотянуться кнопки может он седьмого этажа',
                         'в выше ему ехал кнопку который лифте нажать ним помогал с человек',
                         'выше до дотягивался думаю кнопки не он седьмого этажа я',
                         'выше ему кнопку кто нажать помогал то', 'был обычным он самым человеком',
                         'была было возможность выше ему кнопку лет меньше нажать пяти седьмого у человека этажа этого',
                         'он особенный человек',
                         'выше до до дотягивался дотянуться кнопки кнопок мог не нее но седьмого человек этажа',
                         'была возможность выше кнопку нажать седьмого у человека этажа этого',
                         'а выше до дотягивался кнопки не он седьмого этажа', 'девятого кнопка ли работает этажа',
                         'девятого ему кнопку нажимать помогали этажа',
                         'выше ему кнопку нажать помогали седьмого этажа', 'были него особенности свои у',
                         'верхнего до дотянуться кнопки мог он этажа', 'он особенный',
                         '9 ему кнопку нажимать помогали этажа', '7 выше ему кнопку на нажать помогали этажа',
                         'была выше девятого кнопка кнопки седьмого этажа',
                         'выше до дотягивался кнопки может не он седьмого этажа',
                         'выше девятого кнопка кнопки находилась седьмого этажа этажа',
                         '9 в до едет если кемто лифте может он поехать с этажа',
                         'верхних до дотянуться кнопки мог он этажей',
                         'была девятого кнопка кнопки ниже седьмого этажа этажа',
                         'девятого до дотянуться кнопки может он этажа', 'девятого заела кнопка этажа',
                         'может не он физически', 'был он особенным', 'может нажать не он',
                         'были в него особенности росте серьезные у',
                         'девятого кнопка кнопки находилась ниже седьмого этажа этажа',
                         'высоких до дотягивался кнопки он этажей', 'выше ему кнопку на нажать помогали седьмого этажа',
                         'выше до дотягивался кнопки не он полагаю седьмого этажа я',
                         'в до если есть еще кто лифте может на нем он поехать своего то только этажа', 'заела кнопка',
                         'его ему кнопку нажать помогали этажа',
                         'вероятно выше до дотягивался кнопки не он седьмого этажа',
                         'была возможность выше до дотянуться кнопки него седьмого у этажа',
                         'выше до дотягивался кажется кнопки мне не он седьмого этажа',
                         'до едет кем когда конца он он с то', 'девятого кнопка работает этажа',
                         'а выше до дотягивался кнопки может не он седьмого этажа',
                         'верхних до дотянуться кнопки мог человек этажей', '2 9 для кнопки нужен он'}, False, False
                    ]
                },
                'Безносая смерть': {
                    'То, что прошло 3 месяца - важно': [
                        {'3 зимой месяца с сязанны', '3 время года месяца это', '3 важно месяца',
                         '3 важно именно ли месяца', '3 важно именно месяца', 'время значение имеет',
                         '3 внимание именно месяца на необходимо обращать', '3 важно именно ли месяца что',
                         '3 время года какое месяца то это', '3 временами года месяца с связаны', '3 важно месяца это',
                         '3 месяца определённый период это', '3 зима месяца это', '3 важно именно месяца это',
                         '3 внимание месяца на необходимо обращать', '3 важно именно месяца что',
                         '3 3 внимание вниманиена именно месяца месяца на нужно нужно обращать обращать',
                         '3 время время года года3 месяца месяца одно это это', '3 года месяца свременем связанны',
                         '3 важно именно месяца', '3 важно ли месяца он то умер через что'},
                        False, False
                    ],
                    'он не живое сущесво': [
                        {'неживой он', 'неживой предмет это', 'неодушевленное оно', 'неодушевленное это',
                         'неодушевленный предмет этот', 'неодушевленный он', 'неживое это',
                         'живое не предмет существо это', 'неживой это', 'неживое оно', 'живое не оно существо',
                         'неживое существо это', 'неживое он существо'},
                        False, False
                    ],
                    'он бывает только зимой': [
                        ['зимой предмет существует только этот', 'бывает зимой он только', 'бывает в зиму он только',
                         'быть зимой может предмет только этот', 'бывает зимой предмет только этот',
                         'бывает зимой только это', 'зимой он существует только', 'бывает зимой ситуация только эта',
                         'зимой он только', 'зимой предмет только этот', 'быть в зиму может он только',
                         'зимняя ситуация только это', 'быть в зиму может оно только', 'бывает в зиму только это',
                         'бывает в зиму предмет только это', 'быть зимой может он только',
                         'зимой существует только это', 'быть зимой может только это', 'зимой оно существует только',
                         'зимой ситуация только эта', 'быть в зиму может ситуация только эта',
                         'бывает зимой оно только', 'зимой только это', 'быть в зиму может только это',
                         'зимой оно только', 'бывает в зиму оно только', 'быть зимой может оно только',
                         'быть в зиму может только это', 'быть в зиму может предмет только этот'],
                        False, False
                    ]
                }
            }
        }
        if 'Yandex' in req['meta']['client_id']:
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

                if yes_or_no(req, res, user_id, sessionStorage[user_id]['action'],
                             'Ты знаешь правила игры?', hello_txt) is True:
                    res['response']['text'] = 'Хорошо! Выбери Данетку:\n' + Dan_keys_txt

                elif yes_or_no(req, res, user_id, sessionStorage[user_id]['action'],
                               'Ты знаешь правила игры?', hello_txt) is False:

                    res['response']['text'] = rules_txt + ' Теперь выбери Данетку:\n' + Dan_keys_txt
                elif yes_or_no(req, res, user_id, sessionStorage[user_id]['action'],
                               'Ты знаешь правила игры?', hello_txt) == 'ya':
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
                if sessionStorage[user_id]['game'] == 'ya':
                    return
                elif sessionStorage[user_id]['game'] is None:
                    res['response']['text'] = 'Я не знаю такую Данетку, скажи ещё раз\n' + Dan_keys_txt
                else:  # Функция вернула название Данетки => продолжаем

                    text = Danetki[sessionStorage[user_id]['game']]['question']

                    res['response']['text'] = text
                    res['response']['tts'] = Danetki[sessionStorage[user_id]['game']]['sound'] + text
                    sessionStorage[user_id]['action'] = 'play'

            elif sessionStorage[user_id]['action'] == 'play':
                # Начинается игра. Алиса читает условие Данетки.
                play(req, res, user_id)

        elif sessionStorage['OS'] == 'display':
            if sessionStorage[user_id]['action'] is None:

                # Если поле sessionStorage[user_id]['action'] пустое,
                # значит на данный момент пользователь либо не начал,
                # либо только что закончил отгадывать Данетку.

                if yes_or_no(req, res, user_id, None, 'Ты знаешь правила игры?', hello_txt) is True:
                    res['response']['text'] = 'Хорошо! Выбери режим игры:\n\nИграть с Алисой\nИграть с друзьями'
                    res['response']['tts'] = 'Хорошо! Выбери режим игры: Играть с Алисой или Играть с друзьями'

                elif yes_or_no(req, res, user_id, None, 'Ты знаешь правила игры?', hello_txt) is False:
                    res['response']['text'] = rules_txt + '\n\n' + \
                                              'Выбери режим игры:\n\nИграть с Алисой\nИграть с друзьями'

                elif yes_or_no(req, res, user_id, None, 'Ты знаешь правила игры?', hello_txt) == 'ya':
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
                    if sessionStorage[user_id]['game'] == 'ya':
                        sessionStorage[user_id]['game'] = None
                        return
                    elif sessionStorage[user_id]['game'] is None:
                        res['response']['text'] = 'Я не знаю такую Данетку, скажи ещё раз\n' + Dan_keys_txt
                    else:  # Функция вернула название Данетки => продолжаем

                        text = Danetki[sessionStorage[user_id]['game']]['question']
                        if sessionStorage[user_id]['game_mode'] == 'multi_player':
                            image = Danetki[sessionStorage[user_id]['game']]['image']
                            description = text + '\n\nОтвет на фотографии\n'

                        if sessionStorage[user_id]['game_mode'] == 'multi_player':
                            res['response']['card'] = dict()
                            res['response']['card']['type'] = 'BigImage'
                            res['response']['card']['image_id'] = image
                            res['response']['card']['description'] = description
                            res['response']['tts'] = Danetki[sessionStorage[user_id]['game']]['sound'] + description
                        else:
                            res['response']['text'] = text
                            res['response']['tts'] = Danetki[sessionStorage[user_id]['game']]['sound'] + text

                        sessionStorage[user_id]['action'] = 'play'

            elif sessionStorage[user_id]['action'] == 'play':

                # Начинается игра. Алиса читает условие Данетки.

                if sessionStorage[user_id]['game_mode'] == 'single_player':
                    play(req, res, user_id)
                elif sessionStorage[user_id]['game_mode'] == 'multi_player':
                    if wait_user_answer(req, res, user_id, 'play', 'Продолжайте разгадывать Данетку') == 1:
                        res['response']['text'] = 'Отлично! Вы молодцы. Хотите ещё Данетку?'
                        res['response']['tts'] = '<speaker audio="alice-sounds-game-win-3.opus">' + \
                                                 'Отлично! Вы молодцы. Хотите ещё Данетку?'
                        sessionStorage[user_id]['action'] = 'end_Dan'

            elif sessionStorage[user_id]['action'] == 'end_Dan':
                if yes_or_no(req, res, user_id, 'end_Dan', 'Хотите ещё Данетку?', '') is True:
                    res['response']['text'] = 'Хорошо, секунду. Вы помните правила?'
                    sessionStorage[user_id]['action'] = None
                    sessionStorage[user_id]['game_mode'] = None
                    sessionStorage[user_id]['game'] = None
                elif yes_or_no(req, res, user_id, 'end_Dan', 'Хотите ещё Данетку?', '') is False:
                    res['response']['text'] = 'Приятно было поиграть, пока-пока'
                    res['response']['end_session'] = True
                elif yes_or_no(req, res, user_id, 'end_Dan', 'Хотите ещё Данетку?', '') == 'ya':
                    return
                else:
                    res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому или, если что-то ' \
                                              'не так, скажи "Помощь"\n\nХотите ещё Данетку?'
        return


def game_mode(req, res, user_id):
    # Функция узнаёт и передёт в sessionStorage[user_id]['game_mode']
    # режим игры (однопользовательский или многопользовательский).

    or_ut = req['request']['command'].lower().replace('ё', 'е')
    for single in single_player_list:
        if single in or_ut:
            res['response']['text'] = random.choice(['Отлично!', 'Хорошо!', 'Поняла,']) + \
                                      ' теперь выбери Данетку:\n' + Dan_keys_txt
            return 'single_player'
    for multi in multi_player_list:
        if multi in or_ut:
            res['response']['text'] = multi_rules_txt + '\n\n' + random.choice(['Отлично!', 'Хорошо!', 'Поняла,']) + \
                                      ' Теперь выберите Данетку:\n' + Dan_keys_txt
            return 'multi_player'

    if check_another_oper(req, res, user_id, 'select_mode', game_mode_txt, game_mode_txt) is False:
        res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому'
    return
    # Функция вернёт True, если ответ положительный
    # и вернёт False, если ответ отрицательный


def select(req, res, user_id):
    # Функция узнаёт и передаёт в sessionStorage[user_id]['game']
    # ту Данетку, которую выбрал пользователь.

    or_ut = req['request']['command'].lower().replace('ё', 'е')
    for key in Danetki.keys():
        if or_ut in key.lower():
            res['response']['text'] = random.choice(['Отлично! ', 'Хороший выбор! ']) + Danetki[key]['question']
            res['response']['tts'] = Danetki[key]['sound'] + random.choice(['Отлично! ', 'Хороший выбор! ']) + \
                                     Danetki[key]['question']
            return key

    if check_another_oper(req, res, user_id, 'select_mode', select_txt, select_txt) is True:
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


def yes_or_no(req, res, user_id, action, text, repeate_txt):
    or_ut = req['request']['command'].lower().replace('ё', 'е')

    # Функция вернёт True, если ответ положительный
    # и вернёт False, если ответ отрицательный
    for y in Yes_list:
        if y in or_ut:
            return True
    for n in No_list:
        if n in or_ut:
            return False
    if check_another_oper(req, res, user_id, action, text, repeate_txt) is False:
        res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи "Да" или "Нет" или, ' \
                                  'если что-то не так, скажи "Помощь"'
        return
    elif check_another_oper(req, res, user_id, action, text, repeate_txt) is True:
        return 'ya'


def txt_nat(text):
    text = text.replace(",", "")
    text = text.replace("я знаю что", "")
    text = text.replace("я придумал,", "")
    text = text.replace("я думаю, что", "")
    text = text.replace("мне кажется что", "")
    text = text.replace("друг сказал что", "")
    text = text.replace("мне подсказали что", "")
    text = text.replace("я считаю что", "")
    text = text.replace("я считаю", "")
    text = text.replace("может быть", "")
    text = text.replace(" возможно ", "")
    text = text.replace(" типа ", "")
    text = text.replace("вообще", "")
    text = text.replace("ё", "е")
    text = text.replace(" мне кажется ", "")
    # Избавляемся от лишнего в
    # тексте для дальнейшей обработки.

    return text


###############################
# Функции из standart_functions
###############################


def check_another_oper(req, res, user_id, action, text, repeate_txt):
    # Функция проверяет, вызывал ли пользователь
    # что-либо из standart_functions

    or_ut = req['request']['command'].lower().replace('ё', 'е')
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
    for word in Repeate_list:  # Повтори
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
    return use_stand_func(ret, res, user_id, action, text, repeate_txt)


def use_stand_func(ret, res, user_id, action, text, repeate_txt):
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
            res['response']['text'] = repeate_txt
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
        if Hints[hint][2] is True:
            res['response']['text'] += hint + '\n'
    if res['response']['text'][-2] == ':':
        res['response']['text'] = 'Пока что ты не узнал ничего особенного об этой Данетке.'
    return


def hint(res, user_id):
    try:
        Hints = sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']]
        for hint in Hints:
            if Hints[hint][1] is False:
                sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']][hint][1] = True
                res['response']['text'] = hint
                return
        res['response']['text'] = 'Прости, подсказки закончились. Попробуй по-другому формулировать свои ' \
                                  'вопросы и у тебя всё получится'
        return
    except:
        res['response']['text'] = 'Данетка ещё не выбрана'
        return


def play(req, res, user_id):
    answer = Alice_anwer(req, res)

    if answer == 1:
        res['response']['text'] = random.choice(['Да', 'Верно!', 'Ага', 'Угу', 'Так точно!', 'Ты на верном пути', 'Прекрасно!'])
    elif answer == 2:
        res['response']['text'] = random.choice(['А вот и нет', 'Нет', 'Нет, не то', 'Увы, нет', 'К сожалению, нет'])
    elif answer == 3:
        res['response']['text'] = 'Да! Именно! Если хочешь ещё Данетку, скажи: "Алиса, я хочу другую Данетку".'
        res['response']['tts'] = '<speaker audio="alice-sounds-game-win-3.opus">' + \
                                 'Да! Именно! Если хочешь ещё Данетку, скажи: "Алиса, я хочу другую Данетку".'
    elif answer == 4:
        return
    elif answer == 5:
        res['response']['text'] = random.choice(['Не имеет значения', 'Это неважно'])
    if single_final(user_id) is True:
        res['response']['text'] = 'Кажется, ты уже знаешь всё о Данетке. Попробуй сказать весь ответ полностью, ' \
                                  'если не получается - скажи: "Алиса, что я уже знаю?"'
    return


def Alice_anwer(req, res):
    user_id = req['session']['user_id']
    danetka = sessionStorage[user_id]['game']
    Hints = sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']]
    or_ut = ' '.join(sorted(txt_nat(req['request']['command']).lower().split()))
    if ' не ' in or_ut:
        or_ut_ne = txt_nat(or_ut.replace(' не ', ' ')).lower()
        or_ut_ne = or_ut_ne.replace('не ', '')
    else:
        or_ut_ne = txt_nat(' '.join(sorted((or_ut + ' не').split()))).lower()
    if or_ut in Danetki[danetka]['answers']:
        return 3
    elif or_ut in Danetki[danetka]['yes'] or or_ut_ne in Danetki[danetka]['no']:
        for hint in Hints:
            if or_ut in Hints[hint][0]:
                sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']][hint][1] = True
                sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']][hint][2] = True
        return 1
    elif or_ut in Danetki[danetka]['no'] or or_ut_ne in Danetki[danetka]['yes']:
        return 2
    elif check_another_oper(req, res, user_id, 'play', 'Отлично, продолжай разгадывать Данетку', '') is True:
        return 4
    else:
        return 5


def wait_user_answer(req, res, user_id, action, text):
    user_answer = req['request']['command'].lower().replace('ё', 'е')

    for word in Multi_complete_list:
        if word in user_answer:
            return 1
    if check_another_oper(req, res, user_id, action, text, '') is True:
        return
    else:
        res['response']['text'] = 'Прости, я не поняла твой ответ. Скажите, когда вы разгадаете ' \
                                  'Данетку или, если что-то не так, скажите "Помощь"'
        return


def single_final(user_id):
    Hints = sessionStorage[user_id]['for_hints'][sessionStorage[user_id]['game']]

    for hint in Hints:
        if Hints[hint][2] is False:
            return False
    else:
        return True


if __name__ == '__main__':
    app.run()
