from flask import Flask, request
import logging
import json
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# Создаём ключевой словарь, он будет помогать программе
# ориентироваться между разными моментами работы навыка
sessionStorage = {}

Danetki = {
    'Девушка в автобусе': ['Девушка заходит в автобус. Катя уступает ей своё место, но девушка сильно смутилась.'
                           ' Что стало причиной смущения?', 'Девочка Катя сидела на коленках у свего папы'],
    'Фрэнк и приступ': ['Фрэнк на работе умирает от сердечного приступа. Его коллеги находятся рядом с ним '
                        'в этот момент, однако не оказывают ему помощь. Почему?'],
    'Загадочный человек': ['Некий человек живет на девятом этаже, но когда он возвращается домой, '
                           'то едет на лифте только до седьмого этажа, а дальше идет по лестнице. '
                           'Почему он это делает?', 'Он - карлик.'],
    'Удивительный парашютист': ['Человек выпрыгнул из самолета без парашюта, но остался жив. Как он это сделал?',
                                'Самолёт стоял на земле']
}  # Словарь с Данетками
Dan_keys = 'Девушка в автобусе\nФрэнк и пристуа\nЗагадочный человек\nУдивительный парашютист'  # Для вывода названий
Yes = ["да", "а то", "а как же", "конечно", "хорошо", "ну да", "ещё бы", "точно", "вот именно",
       "легко", "ладно", "ясно", "так точно", "типа того", "разумеется", "правильно", "само собой разумеется",
       "пусть будет так", "безусловно", "ага", "отлично", "несомненно", "реально", "угу", "есть такое дело",
       "однозначно", "неужто", "железобетонно", "а то как же", "ну конечно", "дадада", "дада", "дас", "да с",
       "йес", "поехали", "погнали", "полетели", "давай", 'го']  # Список положительных ответов
No = ["нет", "что вы", "как можно", "что ты", "ни в коем случае", "вот ещё", "ни за что", "очень надо",
      "очень нужно", "ещё чего", "нельзя", "не тутто было", "ничего подобного", "ни фига", "ни капли", "ни хрена",
      "вовсе нет", "как бы не так", "да вы что", "я бы не сказал", "я бы не сказала", "речи быть не может",
      "и речи быть не может", "какое там", "кого там", "куда там", "обойдёшься", "отнюдь", "нету", "не скажи",
      "ни в коем разе", "да нет же", "да нет", "а вот и нет", "нет как нет", "и в помине нет", "чёрта с два",
      "ничуть", "никак нет", "ни под каким видом", "ни шиша", "и в помине нет", "и речи быть не может",
      "ни за что на свете", "хоть убей", "не царское это дело", "ага конечно", "хрен тебе", "ни в жизнь", "шутишь",
      "неа", "и не подумаю", "нетнет", "нетушки"]  # Список отрицательный ответов
rules = '«Данетки» – отличное развлечение для тех, кто любит детективы и ' \
        'логические игры. Я расскажу тебе ситуацию, а тебе нужно отгадать ' \
        'контекст, задавая вопросы, на которые смогу отвечать только "Да" или ' \
        '"Нет". Если тебе понадобится помощь в угадывании ответа, скажи "Подсказка". ' \
        'Если что-то будет непонятно, скажи "Помощь".'  # Правила игры
multi_rules = 'Игра в многопользовательском режиме очень похожа на обычную, но только все задают вопросы одному ' \
              'человеку, который на них отвечает. Когда вы разгадаете Данетку - скажите мне об этом.'


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
        first_name = get_first_name(req)
        # Если не нашли, то сообщаем пользователю, что не расслышали.
        if first_name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        # Если нашли, то приветствуем пользователя
        # и спрашиваем знает ли он правила.
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response']['text'] = 'Приятно познакомиться, ' + first_name.title() + \
                                      '. Я - Алиса. Ты знаешь правила игры?'
            return
    else:
        if sessionStorage[user_id]['action'] is None:

            # Если поле sessionStorage[user_id]['action'] пустое,
            # значит на данный момент пользователь либо не начал,
            # либо только что закончил отгадывать Данетку.

            if yes_or_no(req, res):
                res['response']['text'] = random.choice(['Хорошо!', 'Отлично!', 'Прекасно!']) + \
                                          ' Выбери режим игры:\n\nИграть самому\nИграть с друзьями'
            else:
                res['response']['text'] = rules + '\n\n' + ' Выбери режим игры:\n\nИграть самому\nИграть с друзьями'
            sessionStorage[user_id]['action'] = 'select_mode'
            return

        elif sessionStorage[user_id]['action'] == 'select_mode':  # Выбор режима игры
            if sessionStorage[user_id]['game_mode'] is None:
                sessionStorage[user_id]['game_mode'] = game_mode(req, res)
            else:

                # Блок выбора Данетки.
                # Пользователь называет выбранную Данетку

                sessionStorage[user_id]['game'] = select(req)
                if sessionStorage[user_id]['game'] is not None:

                    text = Danetki[sessionStorage[user_id]['game'].capitalize()][0]
                    answer = Danetki[sessionStorage[user_id]['game'].capitalize()][1]

                    if sessionStorage[user_id]['game_mode'] == 'multi_player':
                        res['response']['text'] = multi_rules + '\n\nА теперь Данетка\n\n' + \
                                                  text + '\n\nОтвет:\n' + answer
                    else:
                        res['response']['text'] = text

                else:
                    res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому или, если что-то ' \
                                              'не так, скажи "Помощь"'

                if sessionStorage[user_id]['game'] is not None:  # Функция вернула название Данетки => продолжаем
                    sessionStorage[user_id]['action'] = 'play'  # Программа переходит в блок игры
            return

        elif sessionStorage[user_id]['action'] == 'play':

            # Начинается игра. Алиса читает условие Данетки.

            if sessionStorage[user_id]['game_mode'] == 'single_player':
                # # Обработка вопросов пользователя
                print("There's nothing at this moment")
            elif sessionStorage[user_id]['game_mode'] == 'multi_player':
                # # Ждём, пока угадают)
                print("There's nothing at this moment")


def game_mode(req, res):
    # Функция узнаёт и передёт в sessionStorage[user_id]['action']['game_mode']
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
    res['response']['text'] = 'Прости, я не поняла твой ответ. Скажи по-другому или, если что-то не так, скажи "Помощь"'
    return
    # Функция вернёт True, если ответ положительный
    # и вернёт False, если ответ отрицательный


def select(req):
    # Функция узнаёт и передаёт в sessionStorage[user_id]['action']
    # ту Данетку, которую выбрал пользователь.
    or_ut = natasha(req['request']['original_utterance']).lower()
    if or_ut.capitalize() in Danetki.keys():
        return or_ut
    else:
        # Если пользователь сказал что-то невнятно, либо
        # выбрал несуществующую историю, Алиса переспросит.
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


def yes_or_no(req, res):
    or_ut = natasha(req['request']['original_utterance']).lower()
    for y in Yes:
        if y in or_ut:
            return True
    for n in No:
        if n in or_ut:
            return False
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
