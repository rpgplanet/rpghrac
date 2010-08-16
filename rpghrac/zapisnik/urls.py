from django.conf.urls.defaults import url, patterns, include

from rpghrac.zapisnik.views import new, home, workshop, edit, preview

urlpatterns = patterns('',
    url("^$", home, name="zapisnik-home"),
    url("^novy/$", new, name="zapisnik-new"),
    url("^(?P<zapisek>\d+)/$", edit, name="zapisnik-edit"),
    url("^(?P<zapisek_id>\d+)/preview/$", preview, name="zapisnik-preview"),
    url("^dilna/$", workshop, name="zapisnik-workshop")
)
