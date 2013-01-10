# -*- coding: utf-8 -*-

import new

from django.http import HttpResponse
from django.db import transaction
from django.utils.translation import ugettext as _

from socketio import socketio_manage
from socketio.mixins import BroadcastMixin
from socketio.namespace import BaseNamespace

from .events import Event
from .signals import socket_connected, socket_disconnected, socket_client_event, socket_client_message, socket_client_event_by_type

def socketio_handler(request):
    socketio_manage(request.environ, {
        '': RootNamespace,
        }, request = request,
    )

    return HttpResponse('')

class RootNamespace(BroadcastMixin, BaseNamespace):
    def recv_connect(self):
        socket_connected.send(sender = self.socket,
            request = self.request, namespace = self)

    def __getattr__(self, name):
        assert name.startswith('on_')

        def fun(self, packet):
            name = packet['name']
            args = packet['args']
            event_id = packet.get('id')
            with transaction.commit_on_success():
                value = self.handle_event(name = name, args = args, event_id = event_id)

            return value

        return new.instancemethod(fun, self, None)


    def recv_disconnect(self):
        socket_disconnected.send(sender = self.socket,
            request = self.request, namespace = self)

    def handle_event(self, name, args, event_id = None):
        request, socket = self.request, self.socket

        message_type = name
        responses = []

        if message_type == 'message':
            responses = socket_client_message.send(sender = socket,
                request = request, message = args)
        else:
            event = Event(socket = socket, namespace = self, name = name,
                args = args, id = event_id)
            kwargs = dict(sender = socket, request = request, event = event,
                namespace = self)
            responses = socket_client_event.send(**kwargs)
            responses.extend(socket_client_event_by_type[event.name].send(**kwargs))

        responses = [response for (receiver, response) in responses if response]
        if responses:
            return responses[0]

