import uuid
import random
import string


def represent_integer(num):
    num = str(num)
    if num[0] in ('-', '+'):
        return num[1:].isdigit()
    return num.isdigit()


def generate_uuid():
    return str(uuid.uuid4())


def _random_string_digits(length=2):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.sample(letters_and_digits, length)).upper()
