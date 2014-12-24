from django.shortcuts import render, redirect, get_object_or_404
from ma3ana_kam_app.models import Expense, Period
import datetime
from ma3ana_kam_app.forms import ExpenseForm, PeriodForm


def index(request):
    now = datetime.datetime.utcnow()
    current_period = Period.objects.get_period_for_date(now)
    current_expenses = Expense.objects.filter(period=current_period)

    return render(request, 'ma3ana_kam_app/index.html', {'period': current_period, 'expenses': current_expenses})


def add_expense(request):
    expense_form = ExpenseForm(request.POST or None)

    if expense_form.is_valid():
        expense_form.save()

        return redirect('/')

    return render(request, 'ma3ana_kam_app/expense_form.html', {'form': expense_form})


def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense_form = ExpenseForm(request.POST or None, instance=expense)

    if expense_form.is_valid():
        expense_form.save()

        return redirect('/')

    return render(request, 'ma3ana_kam_app/expense_form.html', {'form': expense_form})


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == 'POST':
        expense.delete()
        return redirect('/')

    return render(request, 'ma3ana_kam_app/model_delete.html', {'model': expense, 'model_name': 'expense'})


def add_period(request):
    period_form = PeriodForm(request.POST or None)

    if period_form.is_valid():
        period_form.save()
        return redirect('/')

    return render(request, 'ma3ana_kam_app/period_form.html', {'form': period_form})


def update_period(request, pk):
    period = get_object_or_404(Period, pk=pk)
    period_form = PeriodForm(request.POST or None, instance=period)

    if period_form.is_valid():
        period_form.save()
        return redirect('/')

    return render(request, 'ma3ana_kam_app/period_form.html', {'form': period_form})


def delete_period(request, pk):
    period = get_object_or_404(Period, pk=pk)

    if request.method == 'POST':
        period.delete()
        return redirect('/')

    return render(request, 'ma3ana_kam_app/model_delete.html', {'model': period, 'model_name': 'Period'})


def period_list(request, index_number, page_size):
    periods = Period.objects.get_period_list_sliced(index_number, page_size)

    return render(request, 'ma3ana_kam_app/period_list.html', {'periods': periods})