from django.contrib import admin

# Register your models here.

from .models import Site, Building, Floor

admin.site.register(Site)
admin.site.register(Building)
admin.site.register(Floor)
