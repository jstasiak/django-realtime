class Event(object):
    '''
    Represents socket event received from client. 
    '''

    def __init__(self, socket, data):
        self._socket = socket
        self.name = data['name']
        self.data = data.get('args')
        self._event_id = data.get('id')
        self._acknowledged = False

    def acknowledgeable(self):
        '''
        Returns true if event can be acknowledged - it depends on specific socket.emit() call on client
        '''
        return bool(self._event_id)

    def acknowledged(self):
        '''
        Returns true if event has been already acknowledged.
        '''
        return self._acknowledged

    def ack(self, data = None):
        '''
        Confirms reception of the event with optional data passed back to client.
        '''
        assert self.acknowledgeable()
        assert not self.acknowledged()

        self._socket.ack(self._event_id, [data])
        self._acknowledged = True

