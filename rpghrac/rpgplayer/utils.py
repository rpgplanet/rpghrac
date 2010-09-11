from django.views.generic.simple import direct_to_template

def owner_required(func):
    def decorate(request, *args, **kwargs):
        if request.user == request.site_owner:
            return func(request, *args, **kwargs)
        else:
            return direct_to_template(request, '403.html')
    return decorate
