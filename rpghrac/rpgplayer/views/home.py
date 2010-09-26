# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template

#from rpgplayer.forms import LoginForm

def home(request):
    return direct_to_template(request, "home.html", {})

def register(request):
    return direct_to_template(request, "register.html", {})
