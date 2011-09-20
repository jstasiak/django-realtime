# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.db import transaction

from .events import dispatcher, Event

@transaction.commit_manually
def socketio_handler(request):
    try:
        socket = request.environ['socketio']
        connection = Connection(socket)
        connection.handle()
    except Exception as e:
        transaction.rollback()
        raise

    return HttpResponse()


class Connection(object):
    def __init__(self, socket):
        self.socket = socket
        session = socket.session

    def handle(self):
        socket = self.socket

        connect_event = Event(self, dict(name = 'connect'))
        self.handle_event(connect_event)

        while True:
            message = socket.receive()

            # all socket handling runs inside single long-running transaction
            # commit refreshes transaction state
            transaction.commit()

            if message:
                self.handle_message(message)
            else:
                break

            transaction.commit()

        disconnect_event = Event(self, dict(name = 'disconnect'))
        self.handle_event(disconnect_event)

    def handle_message(self, message):
        message_type = message.pop('type')

        if message_type == 'message':
            print('TODO: message_type == message')
        elif message_type == 'event':
            event = Event(self, message)
            self.handle_event(event)

    def handle_event(self, event):
        dispatcher.fire(event)

