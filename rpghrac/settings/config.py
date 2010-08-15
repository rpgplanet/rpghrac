import os
from os.path import dirname, join, abspath
from tempfile import gettempdir

import rpghrac

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ENABLE_DEBUG_URLS = DEBUG

TEST_DATABASE_NAME="test_rpghrac"

SECRET_KEY = 'tlucebubenicektlucenabuben$$$<333changemeasdocumented'

# we want to reset whole cache in test
# until we do that, don't use cache
CACHE_BACKEND = 'dummy://'
CACHE_TIMEOUT = 10*60
CACHE_SHORT_TIMEOUT = 1*60
CACHE_LONG_TIMEOUT = 60*60

NEWMAN_MEDIA_PREFIX = '/static/newman_media/'

SESSION_COOKIE_DOMAIN = '.rpghrac.cz'

MAIN_SUBDOMAIN = 'www'

STATIC_ROOT = abspath(join(dirname(rpghrac.__file__), "static"))

STATIC_URL = "/static/"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)


DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}


DYNAMIC_RPGPLAYER_CATEGORIES = [
#    {
#        "tree_path" : "",
#        "parent_tree_path" : "",
#        "title" : "",
#        "slug" : "",
#    },
    {
        "tree_path" : "rpg",
        "parent_tree_path" : "",
        "title" : "RPG",
        "slug" : "rpg",
    },
]

