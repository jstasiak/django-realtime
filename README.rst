Installation
============

Requirements
------------

* gevent-socketio from `my gevent-socketio repository <https://github.com/jstasiak/gevent-socketio>`_
  (``hg/develop`` branch) and its dependencies
* pip
* git ;)

In Red Hat/CentOS/Fedora they can be obtained by following commands::

    yum install libevent-devel python-setuptools gcc git-core
    easy_install pip
    pip install git+https://jstasiak@github.com/jstasiak/gevent-socketio.git@hg/develop


Installation itself
-------------------

Django-realtime is distributed as setuptools package. To install it with pip execute::

    pip install git+https://jstasiak@github.com/jstasiak/django-realtime.git


Introduction
============
This application allow you to use Socket.IO enabled communication within your Django project.
It uses fairly recent version of Socket.IO - 0.8.4. What I like in Socket.IO > 0.6 is that it has
additional communication channels - events. Every event can be acknowledged with optional return
data which is really nice.

Django-realtime Python package name is simply ``realtime``.

Configuration of your project
-----------------------------

In ``dist`` directory of the package there is ``run.py`` script which can be used to run Django project
using ``gevents PyWSGI`` server. It is required that you run server using this script, I advise that you
copy it to your Django project root directory and run from there.

Server listenson localhost:8000 by default, you can pass ``interface:port`` information in parameter,
like this::

    python run.py 0:8000

Listening on ``0:8000`` means listening on port 8000 on all network interfaces (not only localhost).

Next step is to configure Django project to use ``realtime`` app. To achieve this, you have to:

* add ``realtime`` application to Django ``INSTALLED_APPS`` setting, for example::

    INSTALLED_APPS += ['realtime']

* configure URL dispatcher - you have to put this code in your main ``urls.py`` file::

    urlpatterns += patterns('', url(r'^socket.io/', include('realtime.urls')) )



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

* ``ack(params)`` - functions which confirms receiving event and can be passed some data to send to client in confirmation
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

Acknowledgements
================

I want to thank following people for great code I can use in my projects:

* Jeffrey Gelens and others for `gevent-socketio`_ project
* authors of `Socket.IO`_ project

License
=======

This code is licensed under BSD license. Take it and you it.


.. _gevent-socketio: https://bitbucket.org/Jeffrey/gevent-socketio
.. _socket.io: http://socket.io/