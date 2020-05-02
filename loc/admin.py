'''Definition of admin forms for the `loc` application.'''

from django.contrib import admin

from .models import Plan, Teleport


class TeleportInline(admin.TabularInline):
    '''Inline admin form to edit a teleport.'''

    model = Teleport
    extra = 1
    show_change_link = True
    fields = ['x', 'y', 'text', 'dest']
    fk_name = 'src'


class PlanAdmin(admin.ModelAdmin):
    '''Admin form to edit a plan. Includes the teleport inline form.'''

    fieldset = [
        (None, {'fields': ['name']}),
    ]
    inlines = [TeleportInline]


admin.site.register(Plan, PlanAdmin)
