'''Forms used in the `loc` application.'''

from django import forms

from .models import Plan, Teleport


class PlanForm(forms.ModelForm):
    '''Form to edit plan metadata.'''

    class Meta:
        model = Plan
        fields = ['name', 'image', 'level', 'description', 'address', 'url']

        widgets = {
            'address': forms.Textarea(attrs={'rows': 5}),
            'description': forms.Textarea(attrs={'rows': 5})
        }

        help_texts = {
            'url': ('If there is a website where you can find more information '
                    'related to the plan, store the address here.'),
            'level': ('If the plan represents a floor of a building, use this to '
                      'assign a floor level. This is used to sort the floor '
                      'plans correctly. Otherwise you can keep it empty.')
        }

        labels = {
            'url': 'Web Address',
            'address': 'Physical Address',
            'level': 'Floor Level',
        }




class PlanTeleportForm(forms.ModelForm):
    '''Form to edit a teleport.'''

    class Meta:
        model = Teleport
        fields = ['x', 'y', 'text', 'dest']

        widgets = {
            'x': forms.TextInput(),
            'y': forms.TextInput(),
        }

        labels = {
            'x': 'Relative X Coordinate',
            'y': 'Relative Y Coordinate',
            'dest': 'Teleport Destination',
            'text': 'Teleport Label',
        }

class TeleportDeleteForm(forms.ModelForm):
    '''Form to delete a teleport.'''

    class Meta:
        model = Teleport
        fields = ['text']
