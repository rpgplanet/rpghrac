# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template

#from rpgplayer.forms import LoginForm

def home(request):
    return direct_to_template(request, "home.html", {})

def register(request):
    return direct_to_template(request, "register.html", {})

def logout(request):
    from rpgcommon.user.user import logout, fb_logout

    logout(request=request)

    response = direct_to_template(request, "logout.html", {})

    fb_logout(cookies=request.COOKIES, response=response)

    return response

from django.contrib.auth.views import login as django_login

def login(request):
    res = django_login(request)
    return res
