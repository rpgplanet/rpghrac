from os.path import dirname, join, normpath

import django
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

import ella
from ella import newman

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

from rpgplayer.views.home import home, logout
from django.contrib.auth.views import login

urlpatterns = patterns('',
    # true root is from rpgplayer
    url( r'^$', home, name="root_homepage" ),

    url(r'^prihlas/$', login, name="rpgplayer-login"),
    url(r'^odhlas/$', logout, name="rpgplayer-logout"),
#    url(r'^register/$', register, name="rpgplayer-register" ),

    url('^zapisnik/', include(urls)),

    # ella urls
    url('^tvorba/', include('ella.core.urls')),
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # serve static files
        (r'^%s/(?P<path>.*)$' % settings.STATIC_URL.lstrip('/').rstrip('/'), 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    )


# yes, in tests, models are imported, but not neccessarily when running in production...
# but production must go through http so there so...AAAAAAAARRRRRRRGGGGGHHHHHHHHH!!!!111!
from djangomarkup.register import modify_registered_models
modify_registered_models()

#handler404 = 'ella.core.views.page_not_found'
#handler500 = 'ella.core.views.handle_error'
