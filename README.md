Introduction
=====

Want to make use socket.io inside Django project? Use django-realtime project to make your life easier.

1. Install django-realtime package and its requirements.
2. In your Django project redirect ``socket.io/...`` URL-s to ``realtime.views.socketio_handler`` view like this:

    ```urlpatterns += patterns('', url(r'^socket.io/', include('realtime.urls')))```

1. Subscribe to realtime events:
    
    ```python
    from realtime.events import on_message

    @on_message('connect')
    def handle_connected(event):
        session = event.connection.socket.session
        print('Hooray! User {0} connected!'.format(session.session_id))```
        
1. Enjoy. ;) More documentation coming soon.


***See my URL shortener project using django-realtime: http://github.com/jstasiak/rznij***

Special requirements
====================

* gevent-socketio, it has to be version from hg/develop branch from my repository: http://github.com/jstasiak/gevent-socket.io

License
====

This code is licensed under BSD license, take it and use it.