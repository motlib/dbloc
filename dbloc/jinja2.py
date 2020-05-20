'''Helper for jinja2 template use.'''

from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment

from crispy_forms.utils import render_crispy_form

def environment(**options):
    '''Helper to provide a jinja2 environment.'''
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'crispy': render_crispy_form,
    })

    return env
