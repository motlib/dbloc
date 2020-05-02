'''Views for the `loc` app'''

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .models import Plan
from .forms import PlanMetaForm, PlanTeleportForm
from dbloc import versioninfo


def index(request):
    '''Show the list of sites.'''

    plans = Plan.objects.filter(parent__isnull=True)

    context = {
        'plans': plans,
    }

    return render(request, 'loc/index.html', context)


def plan_details(request, pk):
    '''Show the plan details.'''
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
    '''View to add a new teleport to a plan.'''

    plan = get_object_or_404(Plan, pk=pk)

    if request.method == 'POST':
        form = PlanTeleportForm(request.POST)
        if form.is_valid():
            teleport = form.save(commit=False)
            teleport.src = plan
            teleport.save()

            return redirect('loc:plan', pk=plan.id)
    else:
        form = PlanTeleportForm()

    context = {
        'plan': plan,
        'form': form,
    }

    return render(request, 'loc/plan_add_teleport.html', context)


def search(request):
    '''View for search results.'''

    term = request.GET['term']

    plans = Plan.objects.filter(name__icontains=term).order_by('name').all()

    context = {
        'plans': plans,
        'term': term,
    }

    return render(request, 'loc/search.html', context)


def info(request):
    '''View to show application info.'''

    context = {
        'info': versioninfo,
    }

    return render(request, 'loc/info.html', context)
