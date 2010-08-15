from django.db.models import signals

# we should die in hell for this


from djangomarkup.register import modify_registered_models
signals.post_syncdb.connect(modify_registered_models)

