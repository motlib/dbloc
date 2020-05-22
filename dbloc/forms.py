'''Forms used in the `loc` application.'''

from django import forms

from .models import Plan, Teleport


class PlanMetaForm(forms.ModelForm):
    '''Form to edit plan metadata.'''

    class Meta:
        model = Plan
        fields = ['name', 'image', 'description', 'address', 'url']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 5}),
            'description': forms.Textarea(attrs={'rows': 5})
        }
        help_texts = {
            'url': ('If there is a website where you can find more information '
                    'related to the plan, store the address here.'),
        }

        labels = {
            'url': 'Web Address',
            'address': 'Physical Address',
        }


#class PlanBasicForm(forms.ModelForm):
#    class Meta:
#        model = Plan
#        fields = ['name', 'level']


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
