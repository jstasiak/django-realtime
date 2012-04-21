Notice
======

Beware! This project is highly experimental. It is my personal project which may result in lack
of documentation, lack of my attention due to busy time etc.

Due to its early stage, it's API is subject to change (not drastically, but still).

Please feel free to create an issue if you feel that something should be improved regarding code
or documentation. I also encourage you to hack the source code, it is pretty short and can provide
better understanding of what's going on.

Installation
============

Requirements
------------

* gevent-socketio from `my gevent-socketio repository <https://github.com/jstasiak/gevent-socketio>`_
  (commit ``8835a91dffba4447564ffa30df95663a13e1997e``) and its dependencies
* pip
* django >= 1.3
* git ;)

In Red Hat/CentOS/Fedora they can be obtained by following commands::

    yum install libevent-devel python-setuptools gcc git-core
    easy_install pip
    pip install git+https://jstasiak@github.com/jstasiak/gevent-socketio.git@8835a91dffba4447564ffa30df95663a13e1997e@

You also want to have Socket.IO client, such client in version 0.8.4 is provided by this project.


Installation itself
-------------------

Django-realtime is distributed as setuptools package. To install it with pip execute::

    pip install git+https://jstasiak@github.com/jstasiak/django-realtime.git


Introduction
============
This application allow you to use Socket.IO based communication within your Django project.
It uses fairly recent version of Socket.IO - currently 0.8.4.
What I like in Socket.IO newer than 0.6 is that it has additional communication
channels - events. Every event can be acknowledged with optional return data which is really
nice feature.

It also uses gevent-socketio development version patched by me. Without gevent-socketio this application wouldn't exist.

Some features of django-realtime are inspired by django-socketio project
(https://github.com/stephenmcd/django-socketio). I like django-socketio, but:

* it provides channels (pretty much something like Socket.IO events) by modifying client
  code, I wanted to avoid that
* supports only Socket.IO 0.6, so there is no events and no akcnowledgements (as far as I know)
* has its own event system. django-realtime had such custom system in the past, but I have
  decided to rewrite it to use Django signals and I am happy with that, also it is interface
  which people are familiar with
* I started this project before I discovered django-socketio ;)

Django-realtime Python package name is simply ``realtime``.

Configuration of your project
-----------------------------

Backend
+++++++

Next step is to configure Django project to use ``realtime`` app. To achieve this, you have to:

* add ``realtime`` application to Django ``INSTALLED_APPS`` setting, for example::

    INSTALLED_APPS += ['realtime']

* configure URL dispatcher - you have to put this code in your main ``urls.py`` file::

    urlpatterns += patterns('', url(r'^socket.io/', include('realtime.urls')) )

Frontend
++++++++

If you want to use Socket.IO client provided by django-realtime, put following code in ``HEAD`` section of your HTML template file::

    {% load socketio %}
    {% socketio_client_script %}

Socket.IO client provided by this project is not modified and is provided purely for your convenience. 

Then you probably would write some code actually connecting to server and making use of
Socket.IO client. This is beyond this projects scope, although I present here template
I always take and customize::

    socket = io.connect(null, { transports: ['flashsocket', 'xhr-polling'] });
    socket.on('connect', function() {
        console.log('connected');
    });

    socket.on('disconnect', function() {
        console.log('disconnected');
    });

    socket.on('reconnecting', function() {
        console.log('reconnecting');
    });

    socket.on('reconnect', function() {
        console.log('reconnected');
    });

    socket.on('error', function(e) {
        console.log('error: ' + e);
    });

    socket.on('message', function(message) {
        console.log('received:');
        console.dir(message);
    });

**Warning!** In current development version (it is still correct at 2011-11-16) of
gevent-socketio websocket transport is not working, so to avoid errors please restrict
client transport list so that websocket is not there (like in the example above).


Running server
--------------

Due to high number of possible concurrent and long running connections you cannot use traditional
server like Apache + mod_wsgi to host project using django-realtime. I use gevents pywsgi server.

You can run this server by executing the following command within your project root directory::

    python manage.py rungevent [interface:port]

Interface and port part is optional, it defaults to localhost and 8000.

If you want to be able to connect to the server from remote hosts, enter ``0`` as interface, like
this::

    python manage.py rungevent 0:8000

API
===

Current connections
-------------------

In the top-level of realtime package there is ``connected_sockets`` sequence which contains,
what a surprise, currently connected sockets. These sockets are `gevent-socketio`_ SocketIOProtocol instances.

Usage
+++++

You can for example iterate over it and list connected session ids::

    from realtime import connected_sockets

    print('Connected sockets:')
    for socket in connected_sockets:
        print('- {0}'.format(socket.session.session_id))

When you have reference to connected ``socket`` (obtained from ``realtime.connected_sockets``,
from signal handler parameter ``sender`` or by other means), you can use following methods::

    # sends string 'Hallelujah!' by this particular socket to this particular client
    # signature: socket.send(STRING)
    socket.send('Hallelujah!')

    # emits event named 'notice' with arguments 1, 2 and '!!!'
    # signature: socket.emit(EVENT_NAME, *args)
    socket.emit('notice', 1, 2, '!!!')

    # these are just like socket.send and socket.emit, but send message/event to all
    # clients but this one
    socket.broadcast_send('Hey! New user connected!')
    socket.broadcast_emit('notice', 'Server is shutting down', 'kaboom')

    # acknowledges receiving of an event with particular id
    # signature: socket.ack(EVENT_ID, *args)
    socket.ack('13+', 'event', 'was', 'received', 'blah', 'blah')

In current implementation of ``gevent-socketio``, if message passed to ``socket.send`` is not
basestring instance, it will be converted to its string representation. There is no JSON
encoding here.

On the other hand, arguments supplied to ``socket.emit``, ``broadcast_emit`` and ``socket.ack`` are
JSON encoded.


    
Events
------

Handling input from sockets is based on `Django signals <https://docs.djangoproject.com/en/dev/topics/signals/>`_.
In module ``realtime.signals`` we have:

* ``socket_connected`` - when client connects
* ``socket_disconnected`` - when client disconnects
* ``socket_client_message`` - when you do ``socket.send('some data')`` in the client
* ``socket_client_event`` - fires when you do ``socket.emi('event_name', ...)`` in the client
* ``socket_client_event_by_type`` - dictionary which is indexed by client event name and returns associated signal

In module ``realtime.events`` there is ``Event`` class defined. Its public interface visible for listeners is as follows:

* ``ack(*params)`` - functions which confirms receiving event and can be passed some data to send to client in confirmation
* ``data`` - event data
* ``name`` - name of the event
* ``acknowledgeable()`` - true if this event can be acknowledged
* ``acknowledged()`` - true if this event has been acknowledged already

Usage
+++++

::

    from django.dispatch import receiver
    from realtime.signals import socket_connected, socket_disconnected, socket_client_message, socket_client_event
    @receiver(socket_connected)
    def handle_connected(sender, request, **kwargs):
        socket = sender
        print('{0} connected'.format(socket.session.session_id))
    
    @receiver(socket_disconnected)
    def handle_disconnected(sender, request, **kwargs):
        socket = sender
        print('{0} disconnected'.format(socket.session.session_id))
    
    @receiver(socket_client_message)
    def handle_message(sender, request, message, **kwargs):
        socket = sender
        print('{0} => message {1!r}'.format(socket.session.session_id, message))
    
    
    @receiver(socket_client_event)
    def handle_event(sender, request, event, **kwargs):
        socket = sender
        print('{0} => event {1!r} ({2!r})'.format(socket.session.session_id, event.name, event.data))
        
        if event.acknowledgeable:
            event.ack('I have received your message!')

Example
=======

In project root you can find ``example_chat`` directory. It contains very simple live chat
implementation which uses django-realtime.

I warn you, it is just proof of concept and do not expect it to work flawlessly.


License
=======

This project code is licensed under BSD license unless stated otherwise. Take it and use it.

This repository also contains ``Socket.IO`` client which has its own license.

.. _gevent-socketio: https://bitbucket.org/Jeffrey/gevent-socketio
.. _socket.io: http://socket.io/
