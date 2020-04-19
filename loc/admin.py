from django.contrib import admin

# Register your models here.

from .models import Site, Building, Floor


class FloorInline(admin.TabularInline):
    model = Floor
    extra = 1


class BuildingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'site']}),
    ]
    inlines = [FloorInline]


class BuildingInline(admin.TabularInline):
    model = Building
    extra = 1
    show_change_link = True

class SiteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]
    inlines = [BuildingInline]


admin.site.register(Site, SiteAdmin)
admin.site.register(Building, BuildingAdmin)
#admin.site.register(Floor)
