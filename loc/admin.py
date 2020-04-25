from django.contrib import admin

# Register your models here.

from .models import Plan, Teleport


class TeleportInline(admin.TabularInline):
    model = Teleport
    extra = 1
    show_change_link = True
    fields = ['x', 'y', 'text', 'dest']
    fk_name='src'


class PlanAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['name']}),
    ]
    inlines = [TeleportInline]


#class BuildingAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None, {'fields': ['name', 'site', 'address', 'url']}),
#    ]
#    inlines = [FloorInline, TeleportBuildingInline]


#class BuildingInline(admin.TabularInline):
#    model = Building
#    extra = 1
#    show_change_link = True
#    fieldsets = [
#        (None, {'fields': ['name', 'image']}),
#    ]


#class SiteAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None, {'fields': ['name']}),
#    ]
#    inlines = [BuildingInline]


#admin.site.register(Site, SiteAdmin)
#admin.site.register(Building, BuildingAdmin)
admin.site.register(Plan, PlanAdmin)
