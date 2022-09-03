from django.db import models


def get_key_from_value(dict:dict, value):
    try:
        return next(x for x,y in dict.items() if y == value)
    except:
        return None