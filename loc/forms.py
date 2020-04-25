from django import forms

from .models import Plan, Teleport


class PlanMetaForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['description', 'address', 'url']
        widgets = {
            'address': forms.Textarea(attrs={'cols': 60, 'rows': 6}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 6})
        }


class PlanTeleportForm(forms.ModelForm):
    class Meta:
        model = Teleport
        fields = ['x', 'y', 'text', 'dest']


class PlanSearchForm(forms.Form):
    term = forms.CharField(max_length=200, label='')
