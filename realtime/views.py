# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.db import transaction
from django.utils.translation import ugettext as _

from socketio import socketio_manage
from socketio.namespace import BaseNamespace

from .events import Event
from .signals import socket_connected, socket_disconnected, socket_client_event, socket_client_message, socket_client_event_by_type

def socketio_handler(request):
    value = socketio_manage(request.environ, {
        '': RootNamespace,
        }, request = request,
    )

    return value

class RootNamespace(BaseNamespace):
    def recv_connect(self):
        socket_connected.send(sender = self.socket,
            request = self.request)

    def __getattr__(self, name):
        assert name.startswith('on_')
        name = name.lstrip('on_')
        def f(*args, **kwargs):
            event_id = kwargs.get('event_id')
            with transaction.commit_on_success():
                self.handle_event(name = name, args = args, event_id = event_id)

        return f

    def recv_disconnect(self):
        socket_disconnected.send(sender = self.socket,
            request = self.request)

    def handle_event(self, name, args, event_id = None):
        request, socket = self.request, self.socket

        message_type = name

        if message_type == 'message':
            socket_client_message.send(sender = socket,
                request = request, message = args)
        else:
            event = Event(socket = socket, namespace = self, name = name,
                args = args, id = event_id)
            socket_client_event.send(
                sender = socket, request = request, event = event)
            socket_client_event_by_type[event.name].send(
                sender = socket, request = request, event = event)
