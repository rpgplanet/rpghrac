
def is_site_owner(request):
    return {'is_site_owner' : request.site_owner == request.user }

def site_owner(request):
    return {'site_owner' : request.site_owner }
