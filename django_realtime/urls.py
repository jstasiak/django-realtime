from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    url(r'^.*$', 'views.socketio_handler'),
)
