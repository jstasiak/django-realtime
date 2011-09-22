__version__ = '0.1.1'

from django.dispatch import receiver

from .signals import socket_connected, socket_disconnected

connected_sockets = []

@receiver(socket_connected, weak = False)
def handle_conneceted(sender, request, **kwargs):
    socket = sender
    connected_sockets.append(socket)


@receiver(socket_disconnected, weak = False)
def handle_disconnected(sender, request, **kwargs):
    socket = sender
    connected_sockets.remove(socket)

