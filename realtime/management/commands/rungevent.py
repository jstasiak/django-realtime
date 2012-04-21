# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()

from traceback import print_exc

from django.core.management.base import BaseCommand, CommandError
from django.core.handlers.wsgi import WSGIHandler
from django.core.signals import got_request_exception
from django.utils import autoreload

from socketio import SocketIOServer

def exception_printer(sender, **kwargs):
    print_exc()

class Command(BaseCommand):
    args = '[interface:port]'
    help = 'runs gevent-socketio SocketIOServer'

    def handle(self, *args, **options):
        if len(args) == 1:
            host, port = args[0].split(':')
            port = int(port)
        else:
            host, port = 'localhost', 8000

        autoreload.main(self.main, (host,port))

    def main(self, host, port):
        got_request_exception.connect(exception_printer)

        self.stdout.write('Serving at {host}:{port}\n'.format(host = host, port = port))
        application = WSGIHandler()
        server = SocketIOServer((host, port), application, namespace = 'socket.io', policy_server = False)
        server.serve_forever()


