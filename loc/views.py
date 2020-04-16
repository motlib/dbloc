from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Site, Building


# Create your views here.

def index(request):
    sites = Site.objects.order_by('name')
    template = loader.get_template('loc/index.html')
    context = {
        'sites': sites,
    }

    return HttpResponse(template.render(context, request))


def site(request, site_id):
    try:
        site = Site.objects.get(pk=site_id)
    except Site.DoesNotExist:
        raise Http404("Site not found")

    return render(request, 'loc/site.html', {'site': site})

def building(request, building_id):
    try:
        building = Building.objects.get(pk=building_id)
    except Site.DoesNotExist:
        raise Http404("Building not found")

    return render(request, 'loc/building.html', {'building': building})
