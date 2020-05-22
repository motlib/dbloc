'''Views for the `loc` app'''

from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, \
    DeleteView

from django.forms import inlineformset_factory

from dbloc_project import versioninfo
from .models import Plan, Teleport
from .forms import PlanTeleportForm, PlanForm


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
        context['tp_action'] = 'dbloc:tp_follow'

        return context


class PlanEditView(LoginRequiredMixin, UpdateView):
    '''Edit the metadata of a plan.'''

    model = Plan
    form_class = PlanForm
    template_name = 'dbloc/plan_edit.html'
    context_object_name = 'plan'


class PlanCreateView(LoginRequiredMixin, CreateView):
    '''Create a new top-level plan (i.e. with parent set to null).'''
    model = Plan
    form_class = PlanForm
    template_name = 'dbloc/plan_edit.html'



def plan_delete(request, pk):
    '''Delete a plan. If the plan has sub-plans, reject deleting it.'''

    plan = get_object_or_404(Plan, pk=pk)

    if request.method == 'POST':
        parent = plan.parent
        plan.delete()

        if parent is not None:
            return redirect('dbloc:plan', parent.id)
        else:
            return redirect('dbloc:index')

    else:
        sub_plans = plan.sub_plans

        context = {
            'plan': plan,
            'subplans': sub_plans,
        }

        if len(sub_plans) > 0:
            return render(request, 'dbloc/plan_reject_delete.html', context)
        else:
            return render(request, 'dbloc/plan_confirm_delete.html', context)


def plan_edit_subplans(request, pk):
    plan = get_object_or_404(Plan, pk=pk)

    PlanFormSet = inlineformset_factory(
        parent_model=Plan,
        model=Plan,
        fk_name='parent',
        fields=['id', 'name', 'level'],
        extra=1,
        can_delete=False)

    if request.method == "POST":
        formset = PlanFormSet(request.POST, instance=plan)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return redirect(plan.get_absolute_url())
    else:
        formset = PlanFormSet(instance=plan)

    context = {
        'formset': formset,
        'plan': plan,
    }

    return render(request, 'dbloc/plan_edit_subplans.html', context)



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

            return redirect('dbloc:plan', pk=plan.id)
    else:
        form = PlanTeleportForm()

    context = {
        'plan': plan,
        'form': form,
    }

    return render(request, 'dbloc/plan_edit_teleport.html', context)


def search(request):
    '''View for search results.'''

    term = request.GET['term']
    plans = Plan.objects.filter(name__icontains=term).order_by('name').all()

    context = {
        'plans': plans,
        'title': "Search result: '{0}'".format(term)
    }

    return render(request, 'dbloc/plan_list.html', context)


def info(request):
    '''View to show application info.'''

    context = {
        'info': versioninfo,
    }

    return render(request, 'dbloc/info.html', context)


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

    return render(request, 'dbloc/plan_detail.html', context)


def tp_edit(request, pk):
    '''Edit a teleport'''

    teleport = get_object_or_404(Teleport, pk=pk)

    if request.method == 'POST':
        form = PlanTeleportForm(request.POST, instance=teleport)
        if form.is_valid():
            form.save()

            return redirect('dbloc:plan', pk=teleport.src.id)
    else:
        form = PlanTeleportForm(instance=teleport)

    context = {
        'plan': teleport.src,
        'teleport': teleport,
        'teleports': (teleport,),
        'form': form,
    }

    return render(request, 'dbloc/plan_edit_teleport.html', context)


def tp_follow(request, pk):
    '''Redirect a teleport to the destination plan.'''

    teleport = get_object_or_404(Teleport, pk=pk)

    return redirect('dbloc:plan', pk=teleport.dest.id)


@login_required
def tp_delete(request, pk):
    '''Confirm to delete a teleport.'''

    tp = get_object_or_404(Teleport, pk=pk)

    if request.method == 'POST':
        plan = tp.src
        tp.delete()

        return redirect('dbloc:plan', pk=plan.id)
    else:
        context = {
            'tp': tp
        }
        return render(request, 'dbloc/teleport_confirm_delete.html', context)
