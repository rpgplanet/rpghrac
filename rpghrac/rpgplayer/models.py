from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    slug = models.CharField(max_length=50)
    site = models.ForeignKey(Site, unique=True)
