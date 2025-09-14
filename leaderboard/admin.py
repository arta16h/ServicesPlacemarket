from django.contrib import admin
from django.apps import apps

# Dynamically register all models in this app with a helpful ModelAdmin.
# The admin tries to pick reasonable defaults for list_display, list_filter, search_fields and readonly_fields.
app_config = apps.get_containing_app_config('leaderboard')
models = app_config.get_models()

for model in models:
    try:
        # build sensible list_display: first 6 fields
        fields = [f.name for f in model._meta.fields][:6]
        # list_filter for Boolean/Date/DateTime/ForeignKey fields
        list_filter = [f.name for f in model._meta.fields if f.get_internal_type() in ('BooleanField','DateField','DateTimeField')]
        # search on text-like fields
        search_fields = [f.name for f in model._meta.fields if f.get_internal_type() in ('CharField','TextField')][:4]
        readonly = ['id'] if 'id' in [f.name for f in model._meta.fields] else []

        admin_class = type(f"{model.__name__}AutoAdmin", (admin.ModelAdmin,), {
            'list_display': fields or ['__str__'],
            'list_filter': list_filter,
            'search_fields': search_fields,
            'readonly_fields': readonly,
            'show_full_result_count': False,
        })
        admin.site.register(model, admin_class)
    except Exception as e:
        # If automatic registration fails, try simple register
        try:
            admin.site.register(model)
        except Exception:
            # don't crash admin import
            pass
