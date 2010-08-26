from django.contrib.sites.models import Site
from django.http import Http404
from django.conf import settings

from urlparse import urlparse

from rpgcommon.user.models import UserProfile

class SetDomainOwnerMiddleware:
    def process_request(self, request):
        forced_subdomain = getattr(settings, "RPGHRAC_FORCE_USER_SUBDOMAIN_TO", False)

        bits = urlparse(request.build_absolute_uri()).hostname.split('.')

        request.subdomain_text = forced_subdomain or bits[0]

        # user is not using and subdomain, deny him for now
        if request.subdomain_text == settings.MAIN_SUBDOMAIN:
            raise Http404
        try:
            profile = UserProfile.objects.select_related().get(slug=request.subdomain_text)
            request.site_owner = profile.user
            settings.SITE_ID = profile.site_id
        except UserProfile.DoesNotExist:
            raise Http404

        request.site, create = Site.objects.get_or_create(domain=".".join([request.subdomain_text, settings.SITE_DOMAIN]))
