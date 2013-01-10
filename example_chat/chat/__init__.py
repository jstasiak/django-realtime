from django.dispatch import receiver
from realtime import connected_sockets
from realtime.signals import socket_connected, socket_disconnected, \
    socket_client_event, socket_client_message, socket_client_event_by_type
from realtime.util import failure, success

@receiver(socket_client_event_by_type['echo'])
def handle_echo(sender, request, event, **kwargs):
    return event.args

@receiver(socket_connected)
def handle_connected(sender, request, **kwargs):
    socket = sender
    session = socket.session
    del session['user_name']

@receiver(socket_disconnected)
def handle_disconnected(sender, request, **kwargs):
    socket = sender
    session = socket.session
    namespace = kwargs['namespace']
    if 'user_name' in session:
        namespace.broadcast_event_not_me('system_message', '{0} has left'.format(session['user_name']))

@receiver(socket_client_event_by_type['chat_set_name'])
def handle_set_name(sender, request, event, **kwargs):
    socket = sender
    user_name = event.args[0]
    namespace = kwargs['namespace']

    session = socket.session
    if 'user_name' in session:
        namespace.broadcast_event('system_message', '{0} changed his name to {1}'.format(
            session['user_name'], user_name))
    else:
        namespace.broadcast_event('system_message', '{0} has joined'.format(user_name))

    session['user_name'] = user_name
    return success()


@receiver(socket_client_event_by_type['chat_message'])
def handle_chat_message(sender, request, event, **kwargs):
    socket = sender
    session = socket.session

    message = event.args[0]
    namespace = kwargs['namespace']

    if 'user_name' not in session:
        result = failure()
    else:
        namespace.broadcast_event('chat_message', session['user_name'], message)
        result = success()

    return result
