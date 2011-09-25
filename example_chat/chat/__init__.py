from django.dispatch import receiver
from realtime import connected_sockets
from realtime.signals import socket_connected, socket_disconnected, \
    socket_client_event, socket_client_message, socket_client_event_by_type
from realtime.util import failure, success

@receiver(socket_client_event_by_type['echo'])
def handle_echo(sender, request, event, **kwargs):
    if event.acknowledgeable():
        event.ack(*event.args)

@receiver(socket_connected)
def handle_connected(sender, request, **kwargs):
    socket = sender
    session = socket.session
    session.user_name = None

@receiver(socket_disconnected)
def handle_disconnected(sender, request, **kwargs):
    socket = sender
    session = socket.session
    if session.user_name:
        socket.broadcast_emit('system_message', '{0} has left'.format(session.user_name))

@receiver(socket_client_event_by_type['chat_set_name'])
def handle_set_name(sender, request, event, **kwargs):
    socket = sender
    user_name = event.args[0]

    session = socket.session
    if session.user_name:
        socket.broadcast_emit('system_message', '{0} changed his name to {1}'.format(
            session.user_name, user_name), include_self = True)
    else:
        socket.broadcast_emit('system_message', '{0} has joined'.format(user_name), include_self = True)

    session.user_name = user_name
    event.ack(success())


@receiver(socket_client_event_by_type['chat_message'])
def handle_chat_message(sender, request, event, **kwargs):
    socket = sender
    session = socket.session

    message = event.args[0]

    if not session.user_name:
        event.ack(failure())
    else:
        socket.broadcast_emit('chat_message', session.user_name, message, include_self = True)
        event.ack(success())
