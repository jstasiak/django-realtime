class Event(object):
    '''
    Represents socket event received from client. 
    '''

    def __init__(self, socket, name, namespace = None, args = None, id = None):
        self._socket = socket
        self.name = name
        self.args = args
        self._namespace = namespace
        self._event_id = id
