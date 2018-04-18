# coding=utf-8
import uuid


# from random import choice
# def random_string(length=8, chars=string.letters + string.digits):
#     return ''.join([choice(chars) for i in range(length)])

def random_string(name="default", namespace=uuid.uuid4()):
    name = str(name)
    _string = uuid.uuid3(namespace, name)
    return namespace
