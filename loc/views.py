from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Site, Building, Floor



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
        buildings = site.building_set.order_by('name')
    except Site.DoesNotExist:
        raise Http404("Site not found")

    return render(request, 'loc/site.html', {'site': site, 'buildings': buildings})


def building(request, building_id):
    try:
        building = Building.objects.get(pk=building_id)
        site = building.site
        floors = building.floors
    except Building.DoesNotExist:
        raise Http404("Floor not found")

    return render(request, 'loc/building.html', {
        'floors': floors,
        'building': building,
        'site': site,
        'teleports': building.teleports.all(),
    })


def floor(request, floor_id):
    try:
        floor = Floor.objects.get(pk=floor_id)
        building = floor.building
        site = building.site
    except Floor.DoesNotExist:
        raise Http404("Floor not found")

    return render(request, 'loc/floor.html', {
        'floor': floor,
        'teleports': floor.teleports.all(),
        'building': building,
        'site': building.site,
    })
