from main import natasha
from texts import Multi_complete, Help_f
from standart_functions import *


def wait_user_answer(req, res):
    user_answer = natasha(req['request']['original_utterance']).lower()

    for word in Multi_complete:
        if word in user_answer:
            return 1
    for help in Help_f:
        if help in user_answer:
            return 2
