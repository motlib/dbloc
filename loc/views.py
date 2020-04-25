from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required

from .models import Plan

from .forms import PlanMetaForm, PlanTeleportForm, PlanSearchForm

# Create your views here.

def index(request):
    '''Show the list of sites.'''

    plans = Plan.objects.filter(parent__isnull=True)

    context = {
        'plans': plans,
    }

    return render(request, 'loc/index.html', context)


def plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    context = {
        'plan': plan,
        'parent': plan.parent,
        'sub_plans': plan.plan_set.order_by('name'),
        'teleports': plan.teleports.all(),
    }

    return render(request, 'loc/plan.html', context)


@login_required
def plan_edit_meta(request, pk):
    '''Edit the metadata of a plan.'''

    plan = get_object_or_404(Plan, pk=pk)

    if request.method == "POST":
        form = PlanMetaForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()

            # return to the building view
            return redirect('loc:plan', pk=plan.id)
    else:
        form = PlanMetaForm(instance=plan)

    context = {
        'plan': plan,
        'form': form
    }

    return render(request, 'loc/edit_meta.html', context)

@login_required
def plan_add_teleport(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    if request.method == 'POST':
        form = PlanTeleportForm(request.POST)
        if form.is_valid():
            tp = form.save(commit=False)
            tp.src = plan
            tp.save()

            return redirect('loc:plan', pk=plan.id)
    else:
        form = PlanTeleportForm()

    context = {
        'plan': plan,
        'form': form,
    }

    return render(request, 'loc/plan_add_teleport.html', context)


def search(request):
    form = PlanSearchForm(request.GET)

    if form.is_valid():
        plans = Plan.objects.filter(name__icontains=request.GET['term']).order_by('name').all()
    else:
        form = PlanSearchForm()
        plans = []

    context = {
        'form': form,
        'plans': plans,
    }

    return render(request, 'loc/search.html', context)
