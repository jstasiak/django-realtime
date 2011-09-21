#!/usr/bin/python

from gevent import monkey
monkey.patch_all()

import sys

import os
import traceback

from django.core.handlers.wsgi import WSGIHandler
from django.core.signals import got_request_exception
from django.utils import autoreload

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


def exception_printer(sender, **kwargs):
    traceback.print_exc()

def main():
    got_request_exception.connect(exception_printer)

    if len(sys.argv) > 1:
        host, port = sys.argv[1].split(':')

        if not host:
            host = 'localhost'
        elif host.strip() == '0':
            host = ''

        port = int(port or 8000)
    else:
        host, port = 'localhost', 8000

    print('Serving at {host}:{port}'.format(host = host, port = port))
    application = WSGIHandler()
    server = SocketIOServer((host, port), application, namespace = 'socket.io', policy_server = False)
    server.serve_forever()

if __name__ == '__main__':
    autoreload.main(main)
