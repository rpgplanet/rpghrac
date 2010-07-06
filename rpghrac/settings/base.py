# -*- coding: utf-8 -*-

# Django base settings for rpghrac project.

from os.path import dirname, join

import ella
import django
import rpghrac

DEBUG = False
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Prague'

LANGUAGE_CODE = 'cs'

SITE_ID = 1

USE_I18N = True

ADMIN_ROOTS = (
    join(dirname(ella.__file__), 'newman', 'media'),
    join(dirname(django.__file__), 'contrib', 'admin', 'media'),
)

# List of callables that know how to import templates from various sources.
ROOT_URLCONF = 'rpghrac.urls'

TEMPLATE_DIRS = (
    join(dirname(rpghrac.__file__), 'templates'),
    join(dirname(ella.__file__), 'newman', 'templates'),
)


AUTH_PROFILE_MODULE = 'rpgplayer.UserProfile'
LOGIN_REDIRECT_URL = '/'
SITE_DOMAIN = "rpghrac.cz"

from rpgcommon.settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    'rpghrac.rpgplayer.context_processors.is_site_owner',
    'rpghrac.rpgplayer.context_processors.site_owner',
)