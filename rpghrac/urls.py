from os.path import dirname, join, normpath

import django
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login

import ella
from ella import newman

from rpgplayer.views.home import home, register
from rpghrac.zapisnik import urls

admin.autodiscover()
newman.autodiscover()


#urlpatterns = patterns('',)

ADMIN_ROOTS = (
    normpath(join(dirname(ella.__file__), 'newman', 'media')),
    normpath(join(dirname(django.__file__), 'contrib', 'admin', 'media')),
)

js_info_dict = {
    'packages': ('ella.newman',),
}

urlpatterns = patterns('',
    # true root is from rpgplayer
    url( r'^$', home, name="root_homepage" ),

    url(r'^prihlas/$', login, name="rpgplayer-login"),
#    url(r'^register/$', register, name="rpgplayer-register" ),

    url('^zapisnik/', include(urls)),

    # ella urls
    url('^tvorba/', include('ella.core.urls')),

    # serve static files
    url(r'^%s/(?P<path>.*)$' % settings.TEST_MEDIA_URL.strip('/'), 'django.views.static.serve', {'document_root': settings.TEST_MEDIA_ROOT, 'show_indexes': True}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # serve static files
        (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'), 'django.views.static.serve', {'document_root': settings.TEST_MEDIA_ROOT, 'show_indexes': True}),
    )



handler404 = 'ella.core.views.page_not_found'
handler500 = 'ella.core.views.handle_error'
