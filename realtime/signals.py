from collections import defaultdict

from django.dispatch import Signal

socket_connected = Signal(providing_args = ['request'])
socket_disconnected = Signal(providing_args = ['request'])
socket_client_message = Signal(providing_args = ['request', 'message'])
socket_client_event = Signal(providing_args = ['request', 'event'])

socket_client_event_by_type = defaultdict(lambda: Signal(providing_args = ['request', 'event']))
