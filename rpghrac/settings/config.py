import os
from os.path import dirname, join
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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
TEST_MEDIA_ROOT = MEDIA_ROOT = join(dirname(rpghrac.__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
TEST_MEDIA_URL = MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin_media/'

# Make this unique, and don't share it with anybody.
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

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/site_media/static/"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

#LOGIN_URL = "/account/login/"
#LOGIN_REDIRECT_URLNAME = "what_next"


DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}
