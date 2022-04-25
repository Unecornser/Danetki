from texts import *
from main import natasha, sessionStorage


def check_another_oper(req, res, user_id):
    # Функция проверяет, вызывал ли пользователь
    # что-либо из standart_functions

    or_ut = natasha(req['request']['original_utterance']).lower()
    ret = 0
    for word in Help_f:  # Помощь
        if word in or_ut:
            ret = 1
    for word in Comm_f:  # Команды
        if word in or_ut:
            ret = 2
    for word in An_Dan_f:  # Другая Данетка
        if word in or_ut:
            ret = 3
    for word in Repeate_f:  # Повторить Данетку
        if word in or_ut:
            ret = 4
    for word in Wt_i_kn_f:  # повтор вопросов пользователя с ответом "да"
        if word in or_ut:
            ret = 5
    for word in Hint_f:  # Подсказка
        if word in or_ut:
            ret = 6
    for word in Rules_f:  # Правила
        if word in or_ut:
            ret = 7
    use_stand_func(ret, res, user_id)


def use_stand_func(ret, res, user_id):
    # Выполняется нужная функция исходя из
    # результатов проверки в check_another_oper()

    if ret == 0:
        return False
    elif ret == 1:
        help(res)
    elif ret == 2:
        commands(res)
    elif ret == 3:
        sessionStorage[user_id]['action'] = None
    elif ret == 4:
        repeate_Dan(res, user_id)
    elif ret == 5:
        res['response']['text'] = 'Эта функция ещё не написана'
        print('Эта функция ещё не написана')
        # what_i_know()
    elif ret == 6:
        res['response']['text'] = 'Эта функция ещё не написана'
        print('Эта функция ещё не написана')
        # hint()
    elif ret == 7:
        res['response']['text'] = rules
    return True


def help(res):
    # Алиса говорит, как можно решить какую-либо проблему

    res['response']['text'] = 'Если у Вас проблемы с работой навыка, скажите: "Алиса, хватит" и запустите навык снова. ' \
                              'Если Вы не можете разгадать Данетку, скажите: "Алиса, я хочу другую Данетку. ' \
                              'Если вы хотите узнать, какие команды я знаю, скаиже: "Алиса, команды."'


def commands(res):
    # Алиса расссказывает о командах, которые она знает

    res['response']['text'] = 'Я знаю такие команды: скажи' \
                              '"...Я хочу другую Данетку" - и я дам выбрать тебе другую Данетку. ' \
                              '"...Помощь" - и я расскажу о том, что делать при каки-либо проблемах.' \
                              '"...Хватит" - и я выйду из навыка. ' \
                              '"...Повтори Данетку" - и я прочитаю текущую Данетку снова. ' \
                              '"...Что я уже знаю?" - и я перечислю твои вопросы, на которые я отвечала "да". ' \
                              '"...Что ты умеешь?" - и я расскажу тебе правила моей игры. ' \
                              '"...Подсказка" - и если тебе сложно разгадать Данетку, то я дам тебе подсказку. ' \
                              '"...Команды" - и я скажу какие команды я знаю ' \
                              '"...Правила" - и я расскажи тебе'


def another_Dan(req, res):
    # в поле sessionStorage[user_id]['action'] возвращается None,
    # что возвращает код в состояние выбора режима игры
    return None


def repeate_Dan(res, user_id):
    res['response']['text'] = Danetki[sessionStorage[user_id]['game']]['question']
    return


'''
def what_i_know(res):


def hint(Hints_array, res):
'''