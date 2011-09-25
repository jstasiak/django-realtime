# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.db import transaction
from django.utils.translation import ugettext as _

from .events import Event
from .signals import socket_connected, socket_disconnected, socket_client_event, socket_client_message, socket_client_event_by_type

@transaction.commit_manually
def socketio_handler(request):
    try:
        socket = request.environ['socketio']
        connection = Connection(request = request, socket = socket)
        connection.handle()
    except Exception as e:
        transaction.rollback()
        raise

    return HttpResponse()


class Connection(object):
    def __init__(self, request, socket):
        self._request = request
        self._socket = socket

    def handle(self):
        socket = self._socket
        request = self._request

        socket_connected.send(sender = socket, request = request)

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

        socket_disconnected.send(sender = socket, request = request)

    def handle_message(self, message):
        request, socket = self._request, self._socket
        message_type = message.pop('type')

        if message_type == 'message':
            socket_client_message.send(sender = socket, request = request, message = message['data'])
        elif message_type == 'event':
            event = Event(socket = socket, name = message['name'], args = message.get('args'),
                id = message.get('id'))
            socket_client_event.send(sender = socket, request = request, event = event)
            socket_client_event_by_type[event.name].send(sender = socket, request = request, event = event)
        else:
            assert False, "Should not happen"
             
