'''Forms used in the `loc` application.'''

from django import forms

from .models import Plan, Teleport


#class PlanMetaForm(forms.ModelForm):
#    '''Form to edit plan metadata.'''
#
#    class Meta:
#        model = Plan
#        fields = ['description', 'address', 'url']
#        widgets = {
#            'address': forms.Textarea(attrs={'cols': 60, 'rows': 6}),
#            'description': forms.Textarea(attrs={'cols': 60, 'rows': 6})
#        }
#
#
#class PlanImageForm(forms.ModelForm):
#    '''Form for uploading an image to a plan.'''
#
#    class Meta:
#        model = Plan
#        fields = ['image']


class PlanTeleportForm(forms.ModelForm):
    '''Form to edit a teleport.'''

    class Meta:
        model = Teleport
        fields = ['x', 'y', 'text', 'dest']

        widgets = {
            'x': forms.TextInput(),
            'y': forms.TextInput(),
        }

class TeleportDeleteForm(forms.ModelForm):
    '''Form to delete a teleport.'''

    class Meta:
        model = Teleport
        fields = ['text']
