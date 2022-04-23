import main
import questions
def play(req, res):
    if yes_or_no(req, res):
        res['response']['text'] = 'Да'
    else:
        res['response']['text'] = 'Нет'
    return
def yes_or_no(req, res):
    or_ut = main.natasha(req['request']['original_utterance']).lower()
    or_ut in
    res['response']['text'] = 'Повтори, пожалуйста. Я не поняла твой ответ. Скажи "Да" или "Нет"'
    return