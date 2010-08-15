from django.conf.urls.defaults import *

from djangomarkup.register import modify_registered_models

modify_registered_models()

urlpatterns = patterns('',
)

