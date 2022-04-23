from flask import Flask, request
import logging
import json
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# Создаем словарь, где для каждого пользователя
# мы будем хранить его имя
sessionStorage = {}

Danetki = {
    'девушка в автобусе': ['Девушка заходит в автобус. Катя уступает ей своё место, но девушка сильно смутилась.'
                           ' Что стало причиной смущения?', 'Девочка Катя сидела на коленках у свего папы'],
    'человек из самолета':['Человек выпрыгнул из самолета без парашюта, но остался жив.'
                           'Как он это сделал?', 'Самолет стоял на месте'],
    'френк и приступ':['Фрэнк на работе умирает от сердечного приступ '
                       'Его коллеги находятся рядом с ним в этот момент, однако не оказывают ему помощь.Почему?',
                       'Фрэнк был актером театра и перенес сердечный приступ в середине спектакля.'
                       'Он играл героя, у которого был сердечный приступ.'
                       'Поэтому и его коллеги, и зрители просто подумали, что Фрэнк отличный актер.'],
    'загадочный человек':['Некий человек живет на 9 этаже, но когда он возвращается домой один,'
                          ' то едет на лифте только до 7 этажа и дальше идет по лестнице. Почему он это делает?',
                          'Этот человек карлик и он достает только до кнопки 7 этажа']
}
Yes = ["да", "а то", "а как же", "конечно", "хорошо", "ну да", "ещё бы", "точно", "вот именно",
       "легко", "ладно", "ясно", "так точно", "типа того", "разумеется", "правильно", "само собой разумеется",
       "пусть будет так", "безусловно", "ага", "отлично", "несомненно", "реально", "угу", "есть такое дело",
       "однозначно", "неужто", "железобетонно", "а то как же", "ну конечно", "дадада", "дада", "дас", "да с",
       "йес", "поехали", "погнали", "полетели", "давай", 'го', 'ну го']  # # Список положительных ответов
No = ["нет", "что вы", "как можно", "что ты", "ни в коем случае", "вот ещё", "ни за что", "очень надо",
      "очень нужно", "ещё чего", "нельзя", "не тутто было", "ничего подобного", "ни фига", "ни капли", "ни хрена",
      "вовсе нет", "как бы не так", "да вы что", "я бы не сказал", "я бы не сказала", "речи быть не может",
      "и речи быть не может", "какое там", "кого там", "куда там", "обойдёшься", "отнюдь", "нету", "не скажи",
      "ни в коем разе", "да нет же", "да нет", "а вот и нет", "нет как нет", "и в помине нет", "чёрта с два",
      "ничуть", "никак нет", "ни под каким видом", "ни шиша", "и в помине нет", "и речи быть не может",
      "ни за что на свете", "хоть убей", "не царское это дело", "ага конечно", "хрен тебе", "ни в жизнь", "шутишь",
      "неа", "и не подумаю", "нетнет", "нетушки"]  # # Список отрицательный ответов
rules = '«Данетки» – отличное развлечение для тех, кто любит детективы и ' \
        'логические игры. Я расскажу тебе ситуацию, а тебе нужно отгадать ' \
        'контекст, задавая вопросы, на которые смогу отвечать только "Да" или ' \
        '"Нет". Если тебе понадобится помощь в угадывании ответа, скажи "Подсказка".'  # Правила игры


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
            'action': None
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
        # и спрашиваем знает ли он правила.
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response']['text'] = 'Привет, ' + first_name.title() + '! Я - Алиса. Ты знаешь правила игры?'
            return
    else:
        if sessionStorage[user_id]['action'] is None:

            # Если поле sessionStorage[user_id]['action'] пустое,
            # значит на данный момент пользователь либо не начал,
            # либо только что закончил отгадывать Данетку.

            sessionStorage[user_id]['action'] = 'select'
            if yes_or_no(req, res):
                res['response']['text'] = 'Хорошо! Будем играть?'
            else:
                res['response']['text'] = rules + ' Давай играть?'
            return
        elif sessionStorage[user_id]['action'] == 'select':

            # Сценарий выбора Данетки, тут Алиса озвучивает
            # весь перечень существующих Данеток, после чего
            # пользователь выбирает любую из них.

            if yes_or_no(req, res):
                res['response']['text'] = 'Выбери Данетку: ' + str([e for e in Danetki.keys()])[1:-1]
                sessionStorage[user_id]['action'] = 'select_2'
            else:
                res['response']['text'] = 'Печально...'
            return
        elif sessionStorage[user_id]['action'] == 'select_2':

            # Второй блок выбора Данетки.
            # Тут Алиса запоминает, какую Данетку выбрал пользователь.

            sessionStorage[user_id]['action'] = select(req, res)
            if sessionStorage[user_id]['action'] != 'select_2':
                res['response']['text'] = random.choice(['Отлично! ', 'Хороший выбор! ']) + str(Danetki[sessionStorage[user_id]['action']][0])
                sessionStorage[user_id]['action'] = 'play'
            return
        #elif sessionStorage[user_id]['action'] == 'play':


def select(req, res):
    # Функция узнаёт и передёт в sessionStorage[user_id]['action']
    # ту Данетку, которую выбрал пользователь.

    txt = natasha(req['request']['original_utterance']).lower()
    if txt in Danetki.keys():
        return txt
    else:
        # Если пооьзователь сказал что-то невнятно либо
        # выбрал несуществующую историю, Алиса переспросит.
        res['response']['text'] = 'Я не знаю такую Данетку. Скажи ещё раз.'
        return 'select_2'


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
    text = text.replace("ё", "е")
    # Избавляемся от всех знаков во входящем
    # тексте для дальнейшей обработки.
    # Также меняем "ё" на "е"
    return text


if __name__ == '__main__':
    app.run()
