from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from ma3ana_kam_app.models import Expense, Period
import datetime
from ma3ana_kam_app.forms import ExpenseForm, PeriodForm


@login_required()
def index(request):
    now = datetime.datetime.utcnow()
    try:
        current_period = Period.objects.get_period_for_date(now, request.user)[0]
        current_expenses = Expense.objects.filter(period=current_period)
    except IndexError:
        current_period = None
        current_expenses = None

    return render(request, 'ma3ana_kam_app/period_details.html',
                  {'period': current_period, 'expenses': current_expenses})


@login_required()
def add_expense(request):
    expense_form = ExpenseForm(request.POST or None)
    errors = None

    if request.method == 'POST':
        try:
            expense = expense_form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('/')
        except ValidationError as e:
            errors = e.messages
        except ValueError as e:
            return render(request, 'ma3ana_kam_app/expense_form.html', {'form': expense_form, 'errors': errors})

    return render(request, 'ma3ana_kam_app/expense_form.html', {'form': expense_form, 'errors': errors})


@login_required()
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense_form = ExpenseForm(request.POST or None, instance=expense)

    if not expense.is_belong_to_user(request.user):
        return HttpResponse('Unauthorized', 401)

    if expense_form.is_valid():
        expense_form.save()
        return redirect('/')

    return render(request, 'ma3ana_kam_app/expense_form.html', {'form': expense_form})


@login_required()
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == 'POST':
        expense.delete()
        return redirect('/')

    return render(request, 'ma3ana_kam_app/model_delete.html', {'model': expense, 'model_name': 'expense'})


@login_required()
def add_period(request):
    period_form = PeriodForm(request.POST or None)
    errors = None

    if request.method == 'POST':
        try:
            period = period_form.save(commit=False)
            period.user = request.user
            period.save()

            return redirect('/')
        except ValidationError as e:
            errors = e.messages
        except ValueError:
            return render(request, 'ma3ana_kam_app/period_form.html', {'form': period_form, 'errors': errors})

    return render(request, 'ma3ana_kam_app/period_form.html', {'form': period_form, 'errors': errors})


@login_required()
def update_period(request, pk):
    period = get_object_or_404(Period, pk=pk)
    period_form = PeriodForm(request.POST or None, instance=period)

    if not period.is_belong_to_user(request.user):
        return HttpResponse('Unauthorized', 401)

    if period_form.is_valid():
        period_date = period_form.save(commit=False)
        period_date.user = request.user
        period_date.save()
        return redirect('/')

    return render(request, 'ma3ana_kam_app/period_form.html', {'form': period_form})


@login_required()
def delete_period(request, pk):
    period = get_object_or_404(Period, pk=pk)

    if request.method == 'POST':
        period.delete()
        return redirect('/')

    return render(request, 'ma3ana_kam_app/model_delete.html', {'model': period, 'model_name': 'Period'})


@login_required()
def period_list(request):
    periods = Period.objects.get_period_for_user(request.user)

    paginator = Paginator(periods, 10)
    page = request.GET.get('page')

    try:
        periods_sliced = paginator.page(page)
    except PageNotAnInteger:
        periods_sliced = paginator.page(1)
    except EmptyPage:
        periods_sliced = paginator.page(paginator.num_pages)

    return render(request, 'ma3ana_kam_app/period_list.html', {'periods': periods_sliced})


@login_required()
def period_details(request, pk):
    period = Period.objects.get(pk=pk)
    expenses = Expense.objects.filter(period=period)

    return render(request, 'ma3ana_kam_app/period_details.html', {'period': period, 'expenses': expenses})