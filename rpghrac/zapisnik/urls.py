from django.conf.urls.defaults import url, patterns, include

from rpghrac.zapisnik.views import new, home, workshop, edit

urlpatterns = patterns('',
    url("^$", home, name="zapisnik-home"),
    url("^novy/$", new, name="zapisnik-new"),
    url("^(?P<zapisek>\d+)/$", edit, name="zapisnik-edit"),
    url("^dilna/$", workshop, name="zapisnik-workshop")
)
