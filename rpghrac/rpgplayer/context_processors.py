
def is_site_owner(request):
    if not hasattr(request, "site_owner"):
        owner = False
    else:
        owner = request.site_owner == request.user
    return {'is_site_owner' :  owner}

def site_owner(request):
    # context processor is called even for 404
    if not hasattr(request, "site_owner"):
        return {'site_owner' : None }

    root_category = None

#    try:
#        from django.conf import settings
#        from django.contrib.sites.models import Site
#        from ella.core.models import Category
#
#        root_category = Category.objects.get(
#            site = Site.objects.get(pk=settings.SITE_ID),
#            tree_parent = None
#        )
#    except:
#        raise

    return {
        'site_owner' : request.site_owner,
        'root_category' : root_category
    }
