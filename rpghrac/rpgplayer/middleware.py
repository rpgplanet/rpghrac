from django.http import Http404
from django.conf import settings

from urlparse import urlparse

from rpgplayer.models import UserProfile

class SetDomainOwnerMiddleware:
    def process_request(self, request):
        bits = urlparse(request.build_absolute_uri()).hostname.split('.')
        request.subdomain_text = bits[0]

        #user is not using and subdomain, deny him for now
        if request.subdomain_text == settings.MAIN_SUBDOMAIN:
            raise Http404
        try:
            request.site_owner = UserProfile.objects.select_related().get(slug=request.subdomain_text)
        except UserProfile.DoesNotExist:
            raise Http404
        
