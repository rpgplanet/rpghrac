
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
    return {'site_owner' : request.site_owner }
