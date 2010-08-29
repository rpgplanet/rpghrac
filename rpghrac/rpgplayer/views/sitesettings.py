
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.simple import direct_to_template

from rpgplayer.forms import GeneralSiteSettingsForm
from rpghrac.rpgplayer.models import SiteSettings

def index(request):
    try:
        instance = SiteSettings.objects.get(site=request.site)
    except SiteSettings.DoesNotExist:
        instance = SiteSettings(site=request.site)
        
    if request.method == "POST":
            
        site_form = GeneralSiteSettingsForm(request.POST, instance=instance)

        if site_form.is_valid():
            site_form.save()
            #TODO: OK message
            return HttpResponseRedirect(reverse(index))

    else:
        site_form = GeneralSiteSettingsForm(instance=instance)
        

    return direct_to_template(request, "sitesettings/index.html", {
        "site_form" : site_form,
    })
