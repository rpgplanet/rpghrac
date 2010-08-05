import os
from os.path import dirname, join, abspath
from tempfile import gettempdir

import rpghrac

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ENABLE_DEBUG_URLS = DEBUG

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = join(gettempdir(), 'rpghrac.db')
TEST_DATABASE_NAME = join(gettempdir(), 'rpghrac-test.db')
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

SECRET_KEY = 'tlucebubenicektlucenabuben$$$<333'

SECRET_KEY = '^980$0s46q1(toq*mu23m41_ac_@vwy)+mig=ka_97$m0^fh)v'

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

