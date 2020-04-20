from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Site, Building, Floor

from .forms import BuildingMetaForm, SiteMetaForm

# Create your views here.

def index(request):
    sites = Site.objects.order_by('name')
    template = loader.get_template('loc/index.html')
    context = {
        'sites': sites,
    }

    return HttpResponse(template.render(context, request))


def site(request, pk):
    try:
        site = Site.objects.get(pk=pk)
        buildings = site.building_set.order_by('name')
    except Site.DoesNotExist:
        raise Http404("Site not found")

    return render(request, 'loc/site.html', {'site': site, 'buildings': buildings})


def building(request, pk):
    try:
        building = Building.objects.get(pk=pk)
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


def floor(request, pk):
    try:
        floor = Floor.objects.get(pk=pk)
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


def building_edit_meta(request, pk):
    building = get_object_or_404(Building, pk=pk)

    if request.method == "POST":
        form = BuildingMetaForm(request.POST, instance=building)
        if form.is_valid():
            form.save()
            return redirect('loc:building', pk=building.id)
    else:
        form = BuildingMetaForm(instance=building)

    return render(request, 'loc/edit_meta.html', {'building': building, 'site': building.site, 'form': form})


def site_edit_meta(request, pk):
    site = get_object_or_404(Site, pk=pk)

    if request.method == "POST":
        form = SiteMetaForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            return redirect('loc:site', pk=site.id)
    else:
        form = BuildingMetaForm(instance=site)

    return render(request, 'loc/edit_meta.html', {'site': site, 'form': form})
