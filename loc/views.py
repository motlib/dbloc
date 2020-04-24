from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

from .models import Site, Building, Floor

from .forms import BuildingMetaForm, SiteMetaForm

# Create your views here.

def index(request):
    '''Show the list of sites.'''

    sites = Site.objects.order_by('name')

    context = {
        'sites': sites,
    }

    return render(request, 'loc/index.html', context)


def site(request, pk):
    site = get_object_or_404(Site, pk=pk)

    context = {
        'site': site,
        'buildings': site.building_set.order_by('name'),
    }

    return render(request, 'loc/site.html', context)


def building(request, pk):
    building = get_object_or_404(Building, pk=pk)

    context = {
        'floors': building.floors,
        'building': building,
        'site': building.site,
        'teleports': building.teleports.all(),
    }

    return render(request, 'loc/building.html', context)


def floor(request, pk):
    floor = get_object_or_404(Floor, pk=pk)

    return render(request, 'loc/floor.html', {
        'floor': floor,
        'teleports': floor.teleports.all(),
        'building': floor.building,
        'site': floor.building.site,
    })


@login_required
def building_edit_meta(request, pk):
    '''Edit the metadata of a building.'''

    building = get_object_or_404(Building, pk=pk)

    if request.method == "POST":
        form = BuildingMetaForm(request.POST, instance=building)
        if form.is_valid():
            form.save()

            # return to the building view
            return redirect('loc:building', pk=building.id)
    else:
        form = BuildingMetaForm(instance=building)

    context = {
        'building': building,
        'site': building.site,
        'form': form
    }

    return render(request, 'loc/edit_meta.html', context)


@login_required
def site_edit_meta(request, pk):
    '''Edit the metadata of a site.'''

    site = get_object_or_404(Site, pk=pk)

    if request.method == "POST":
        form = SiteMetaForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            return redirect('loc:site', pk=site.id)
    else:
        form = SiteMetaForm(instance=site)

    context = {
        'site': site,
        'form': form,
    }

    return render(request, 'loc/edit_meta.html', context)
