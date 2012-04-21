from django.conf import settings
from django.template import Library

register = Library()

@register.simple_tag
def socketio_client_script():
    return '<script src="{static_url}js/external/socket.io-0.9.6.js"></script>'.format(static_url = settings.STATIC_URL)

