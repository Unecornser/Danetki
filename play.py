from main import *
from texts import *


def play(req, res, sessionStorage):
    answer = yes_or_no(req, res, sessionStorage)
    if answer == 1:
        res['response']['text'] = 'Да'
    elif answer == 2:
        res['response']['text'] = 'Нет'
    elif answer == 3:
        res['response']['text'] = 'Не имеет значения'
    elif answer == 4:
        res['response']['text'] = 'Пожалуйста, задайте другой вопрос'
    else:
        res['response']['text'] = 'Неизвестный вариант обработки: ' + answer
    return


def yes_or_no(req, res, sessionStorage):
    user_id = req['session']['user_id']
    or_ut = natasha(req['request']['original_utterance']).lower()
    danetka = sessionStorage[user_id]['game']
    if or_ut in Danetki[danetka]['yes']:
        return 1
    elif or_ut in Danetki[danetka]['no']:
        return 2
    elif or_ut in Danetki[danetka]['nothing']:
        return 3
    else:
        return 4
