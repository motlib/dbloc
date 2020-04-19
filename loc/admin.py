from django.contrib import admin

# Register your models here.

from .models import Site, Building, Floor, Teleport

class TeleportBuildingInline(admin.TabularInline):
    model = Teleport
    extra = 1
    show_change_link = True
    fields = ['x', 'y', 'text', 'dest_floor', 'dest_building']
    fk_name = 'src_building'

class TeleportFloorInline(admin.TabularInline):
    model = Teleport
    extra = 1
    show_change_link = True
    fields = ['x', 'y', 'text', 'dest_floor', 'dest_building']
    fk_name = 'src_floor'


class FloorInline(admin.TabularInline):
    model = Floor
    extra = 1
    show_change_link = True


class FloorAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['name']}),
    ]
    inlines = [TeleportFloorInline]


class BuildingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'site', 'address', 'url']}),
    ]
    inlines = [FloorInline, TeleportBuildingInline]


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
admin.site.register(Floor, FloorAdmin)
