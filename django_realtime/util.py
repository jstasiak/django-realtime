# -*- coding: utf-8 -*-

def success(message = None, **kwargs):
    result = dict(kwargs)
    result['success'] = True
    if message:
        result['message'] = message

    return result

def failure(message = None, **kwargs):
    result = dict(kwargs)
    result['success'] = False
    if message:
        result['message'] = message

    return result

