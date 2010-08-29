from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'usersettings/index.html'}, name="usersettings"),
    url(r'^avatar/', include('avatar.urls')),
)

