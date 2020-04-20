from django import forms

from .models import Site, Building


class SiteMetaForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['address', 'url']

class BuildingMetaForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['address', 'url']
