'''Views for the `loc` app'''

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

from dbloc import versioninfo
from .models import Plan
from .forms import PlanMetaForm, PlanTeleportForm


class PlanIndexView(ListView):
    '''Index list of top-level plans'''

    queryset = Plan.objects.filter(parent__isnull=True)
    context_object_name = 'plans'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Top-level Plans'

        return context


class PlanDetailView(DetailView):
    '''Detail view of a plan.'''

    model = Plan
    context_object_name = 'plan'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        plan = context['plan']

        context['parent'] = plan.parent
        context['sub_plans'] = plan.sub_plans
        context['teleports'] = plan.teleports.all()

        return context


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

    return render(request, 'loc/plan_edit_meta.html', context)


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
        'title': "Search result: '{0}'".format(term)
    }

    return render(request, 'loc/plan_list.html', context)


def info(request):
    '''View to show application info.'''

    context = {
        'info': versioninfo,
    }

    return render(request, 'loc/info.html', context)
