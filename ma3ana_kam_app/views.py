from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Period
from .forms import ExpenseForm, PeriodForm
from .utils import paginate_model


@login_required()
def index(request, template_name='ma3ana_kam_app/period_details.html'):
    """
    Home Page
    :param request:
    :param template_name:
    :return:
    """
    current_period = Period.objects.get_today_period(request.user)
    current_expenses = Expense.objects.filter(period=current_period)


    return render(request, template_name,
                  {'period': current_period, 'expenses': current_expenses})


# region Expense
@login_required()
def add_expense(request, template_name='ma3ana_kam_app/expense_form.html'):
    """
    Add new expense view
    :param request:
    :param template_name:
    :return:
    """
    expense_form = ExpenseForm(request.POST or None)
    errors = None

    if request.method == 'POST':
        try:
            expense = expense_form.save(commit=False)
            expense.user = request.user
            expense.save()
            # Add reverse for the URL
            return redirect('/')
        except ValidationError as e:
            errors = e.messages
        except ValueError as e:
            return render(request, template_name, {'form': expense_form, 'errors': errors})

    return render(request, template_name, {'form': expense_form, 'errors': errors})


@login_required()
def update_expense(request, pk, template_name='ma3ana_kam_app/expense_form.html'):
    """
    Update expense view
    :param request:
    :param pk:
    :param template_name:
    :return:
    """
    expense = get_object_or_404(Expense, pk=pk)
    expense_form = ExpenseForm(request.POST or None, instance=expense)

    if not expense.is_belong_to_user(request.user):
        return HttpResponse('Unauthorized', 401)

    if expense_form.is_valid():
        expense_form.save()
        return redirect('/')

    return render(request, template_name, {'form': expense_form})


@login_required()
def delete_expense(request, pk, template_name='ma3ana_kam_app/model_delete.html'):
    """
    delete expense view
    :param request:
    :param pk:
    :param template_name:
    :return:
    """
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('/')

    return render(request, template_name, {'model': expense, 'model_name': 'expense'})


# endregion

# region Period
@login_required()
def add_period(request, template_name='ma3ana_kam_app/period_form.html'):
    """
    Add new period view
    :param request:
    :param template_name:
    :return:
    """
    period_form = PeriodForm(request.POST or None)
    errors = None

    if request.method == 'POST':
        try:
            period = period_form.save(commit=False)
            period.user = request.user
            period.save()
            return redirect(reverse('home'))
        except ValidationError as e:
            errors = e.messages
        except ValueError:
            return render(request, template_name, {'form': period_form, 'errors': errors})

    return render(request, template_name, {'form': period_form, 'errors': errors})

@login_required()
def update_period(request, pk, template_name='ma3ana_kam_app/period_form.html'):
    """
    Update period view
    :param request:
    :param pk:
    :param template_name:
    :return:
    """
    period = get_object_or_404(Period, pk=pk)
    period_form = PeriodForm(request.POST or None, instance=period)

    if not period.is_belong_to_user(request.user):
        return HttpResponse('Unauthorized', 401)

    if request.method == 'POST':
        if period_form.is_valid():
            period_data = period_form.save(commit=False)
            period_data.user = request.user
            period_data.save()
            return redirect(reverse('home'))
    return render(request, template_name, {'form': period_form})

@login_required()
def delete_period(request, pk, template_name='ma3ana_kam_app/model_delete.html'):
    """
    Delete period view
    :param request:
    :param pk:
    :param template_name:
    :return:
    """
    period = get_object_or_404(Period, pk=pk)
    if request.method == 'POST':
        period.delete()
        return redirect(reverse('home'))
    return render(request, template_name, {'model': period, 'model_name': 'Period'})

@login_required()
def period_list(request, template_name='ma3ana_kam_app/period_list.html'):
    """
    Period list view
    :param request:
    :param template_name:
    :return:
    """
    periods = Period.objects.get_user_period(request.user)
    page = request.GET.get('page')
    periods_sliced = paginate_model(periods, page)
    return render(request, template_name, {'periods': periods_sliced})

@login_required()
def period_details(request, pk, template_name='ma3ana_kam_app/period_details.html'):
    """
    Period details (Period + Expense) view
    :param request:
    :param pk:
    :param template_name:
    :return:
    """
    period = Period.objects.get(pk=pk)
    if not period.is_belong_to_user(request.user):
        return HttpResponse('Unauthorized', 401)
    expenses = Expense.objects.filter(period=period)
    return render(request, template_name, {'period': period, 'expenses': expenses})

# endregion
