from django import forms

from .models import Site, Building


class MetadataMeta:
    fields = ['description', 'address', 'url']
    widgets = {
        'address': forms.Textarea(attrs={'cols': 60, 'rows': 6}),
        'description': forms.Textarea(attrs={'cols': 60, 'rows': 6})
    }


class SiteMetaForm(forms.ModelForm):
    class Meta(MetadataMeta):
        model = Site


class BuildingMetaForm(forms.ModelForm):
    class Meta(MetadataMeta):
        model = Building
