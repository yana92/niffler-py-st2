import random
import string


def random_string(length=5):
    """Генерация случайной строки с заданным колличеством символов

    Поумолчанию 5 символов
    """
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
