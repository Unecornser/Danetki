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
    'Девушка в автобусе': ['Девушка заходит в автобус. Катя уступает ей своё место, но девушка сильно смутилась.'
                           ' Что стало причиной смущения?', 'Девочка Катя сидела на коленках у свего папы']
}
Yes = ["да", "а то", "а как же", "конечно", "хорошо", "ну да", "ещё бы", "точно", "вот именно",
       "легко", "ладно", "ясно", "так точно", "типа того", "разумеется", "правильно", "само собой разумеется",
       "пусть будет так", "безусловно", "ага", "отлично", "несомненно", "реально", "угу", "есть такое дело",
       "однозначно", "неужто", "железобетонно", "а то как же", "ну конечно", "дадада", "дада", "дас", "да с",
       "йес", "поехали", "погнали", "полетели"]  # # Список положительных ответов
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
        # и спрашиваем знает ли он правила
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response']['text'] = 'Приятно познакомиться, ' + first_name.title() + '. Я - Алиса. Ты знаешь правила игры?'
            return
    else:
        if not sessionStorage[user_id]['action']:
            if yes_or_no(req):
                res['response']['text'] = 'Хорошо! Тогда давай играть, выбери Данетку:'
                sessionStorage[user_id]['action'] = 'select' # добавляем в sessionStorage action!!!
            else:
                res['response']['text'] = rules + 'Давай играть?'
            return

        else:
            if yes_or_no(req):
                res['response']['text'] = str([e for e in Danetki.keys()])[2:-2]
            else:
                res['response']['text'] = 'Очень жаль...'
            return


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


def yes_or_no(req):
    or_ut = natasha(req['request']['original_utterance']).lower()
    print(or_ut)
    # Функция вернёт True, если ответ положительный
    # и вернёт False, если ответ отрицательный
    return True if or_ut in Yes else False


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
