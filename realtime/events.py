class Event(object):
    def __init__(self, socket, data):
        self._socket = socket
        self.name = data['name']
        self.data = data.get('args')
        self._event_id = data.get('id')
        self._acknowledged = False

    @property
    def acknowledgeable(self):
        return bool(self._event_id)

    @property
    def acknowledged(self):
        return self._acknowledged

    def ack(self, data):
        assert self.acknowledgeable
        assert not self.acknowledged

        self._socket.ack(self._event_id, [data])
        self._acknowledged = True

