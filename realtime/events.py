class Event(object):
    '''
    Represents socket event received from client. 
    '''

    def __init__(self, socket, name, args = None, id = None):
        self._socket = socket
        self.name = name
        self.args = args
        self._event_id = id
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

    def ack(self, *args):
        '''
        Confirms reception of the event with optional data passed back to client.
        '''
        assert self.acknowledgeable()
        assert not self.acknowledged()

        self._socket.ack(self._event_id, *args)
        self._acknowledged = True

