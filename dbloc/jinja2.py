'''Helper for jinja2 template use.'''

from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment


def environment(**options):
    '''Helper to provide a jinja2 environment.'''
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
    })

    return env
