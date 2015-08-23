import datetime
from django import forms
from django.forms import ModelForm, DateInput
from ma3ana_kam_app.models import Expense, Period
from ma3ana_kam.input_types import DateTypeInput


class ExpenseForm(ModelForm):
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
    class Meta:
        model = Period
        fields = ['start_date', 'end_date', 'amount', 'description']
        widgets = {
            'start_date': DateTypeInput(attrs={'class': 'form-control'}),
            'end_date': DateTypeInput(attrs={'class': 'form-control'}),
            'amount': forms.widgets.NumberInput(attrs={'step': 'any', 'class': 'form-control'}),
            'description': forms.widgets.TextInput(attrs={'class': 'form-control'})

        }