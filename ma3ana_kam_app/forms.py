import datetime
from django import forms
from django.forms import ModelForm, DateInput
from .models import Expense, Period, PeriodList
from ma3ana_kam.input_types import DateTypeInput


class ExpenseForm(ModelForm):
    """
    Expense form for update and insert
    """
    date = forms.DateField(initial=datetime.datetime.now().date(),
                           widget=DateTypeInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Expense
        fields = ['id', 'date', 'amount', 'description']
        exclude = ['user', 'period']
        widgets = {
            'amount': forms.widgets.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),
            'description': forms.widgets.TextInput(attrs={'class': 'form-control'})
        }


class PeriodForm(ModelForm):
    """
    Period from for update and insert
    """
    class Meta:
        model = Period
        fields = ['start_date', 'end_date', 'amount', 'description']
        widgets = {
            'start_date': DateTypeInput(attrs={'class': 'form-control'}),
            'end_date': DateTypeInput(attrs={'class': 'form-control'}),
            'amount': forms.widgets.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),
            'description': forms.widgets.TextInput(attrs={'class': 'form-control'})

        }

class PeriodListForm(ModelForm):
    """
    Period List form for update and insert
    """
    class Meta:
        model = PeriodList
        fields = ['name']
        widgets = {
            'name': forms.widgets.TextInput(attrs={'class': 'form-control'})
        }

