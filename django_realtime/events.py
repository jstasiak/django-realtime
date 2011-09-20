# -*- coding: utf-8 -*-

class EventDispatcher(object):
    def __init__(self):
        self._event_handlers_chains = {}

    def handler_chain_for_event(self, event_name):
        chains = self._event_handlers_chains

        if event_name not in chains:
            chains[event_name] = []

        return chains[event_name]

    def bind(self, event_name, handler):
        chain = self.handler_chain_for_event(event_name)
        chain.append(handler)

    def unbind(self, event_name, handler):
        chain = self.handler_chain_for_event(event_name)
        chain.remove(handler)

    def fire(self, event):
        chain = self.handler_chain_for_event(event.name)

        for handler in chain:
            handler(event)

dispatcher = EventDispatcher()

def on_event(event_name):
    def factory(func):
        def decorator(*args, **kwargs):
            func(*args, **kwargs)
        dispatcher.bind(event_name, decorator)

        return decorator

    return factory

class Event(object):
    def __init__(self, connection, data):
        self.acknowledged = False
        self.connection = connection
        self.name = data['name']
        self.args = data.get('args')
        self.event_id = data.get('id')

    @property
    def acknowledgeable(self):
        return bool(self.event_id)

    def ack(self, params):
        assert self.acknowledgeable
        assert not self.acknowledged

        socket = self.connection.socket
        socket.ack(self.event_id, [params])




