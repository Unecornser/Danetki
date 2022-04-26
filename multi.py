'''
from texts import Multi_complete, Help_f
from standart_functions import *


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


def wait_user_answer(req, res):
    user_answer = natasha(req['request']['original_utterance']).lower()

    for word in Multi_complete:
        if word in user_answer:
            return 1
    for help in Help_f:
        if help in user_answer:
            return 2
'''
