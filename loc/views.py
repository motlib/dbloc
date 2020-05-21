'''Views for the `loc` app'''

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView

from dbloc_project import versioninfo
from .models import Plan, Teleport
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
        context['tp_action'] = 'loc:tp_follow'

        return context


class PlanMetaEdit(LoginRequiredMixin, UpdateView):
    '''Edit the metadata of a plan.'''

    model = Plan
    fields = ['address', 'description', 'url']
    template_name = 'loc/plan_edit_meta.html'


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

    return render(request, 'loc/plan_edit_teleport.html', context)


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


# select tp -> edit tp
@login_required
def plan_select_tp(request, pk, tp_action):
    '''Select a teleport for next action (edit, delete)'''

    plan = get_object_or_404(Plan, pk=pk)

    context = {
        'plan': plan,
        'tp_action': tp_action,
        'parent': plan.parent,
        'sub_plans': plan.sub_plans,
        'teleports': plan.teleports.all(),
    }

    return render(request, 'loc/plan_detail.html', context)


def tp_edit(request, pk):
    '''Edit a teleport'''

    teleport = get_object_or_404(Teleport, pk=pk)

    if request.method == 'POST':
        form = PlanTeleportForm(request.POST, instance=teleport)
        if form.is_valid():
            form.save()

            return redirect('loc:plan', pk=teleport.src.id)
    else:
        form = PlanTeleportForm(instance=teleport)

    context = {
        'plan': teleport.src,
        'teleport': teleport,
        'teleports': (teleport,),
        'form': form,
    }

    return render(request, 'loc/plan_edit_teleport.html', context)


def tp_follow(request, pk):
    '''Redirect a teleport to the destination plan.'''

    teleport = get_object_or_404(Teleport, pk=pk)

    return redirect('loc:plan', pk=teleport.dest.id)


@login_required
def tp_delete(request, pk):
    '''Confirm to delete a teleport.'''

    tp = get_object_or_404(Teleport, pk=pk)

    if request.method == 'POST':
        plan = tp.src
        tp.delete()

        return redirect('loc:plan', pk=plan.id)
    else:
        context = {
            'tp': tp
        }
        return render(request, 'loc/teleport_confirm_delete.html', context)
