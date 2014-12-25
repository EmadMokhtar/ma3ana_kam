from django import forms
from django.forms import ModelForm
from ma3ana_kam_app.models import Expense, Period
from ma3ana_kam.input_types import DateTypeInput


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'amount', 'description']
        widgets = {
            'date': DateTypeInput,
            'amount': forms.widgets.NumberInput(attrs={'step': '1'}),
        }

    def clean(self):
        expense_data = super(ExpenseForm, self).clean()
        expense_date = expense_data.get('date')
        period = Period.objects.get_period_for_date(expense_date)
        if not period:
            raise forms.ValidationError('Please check the date, there is no period in this date.')

        return expense_data


class PeriodForm(ModelForm):
    class Meta:
        model = Period
        fields = ['start_date', 'end_date', 'amount', 'description']
        widgets = {
            'start_date': DateTypeInput,
            'end_date': DateTypeInput,
            'amount': forms.widgets.NumberInput(attrs={'step': '1'}),

        }

    def clean(self):
        period_data = super(PeriodForm, self).clean()
        period_start_date = period_data.get('start_date')
        period_end_date = period_data.get('end_date')

        period_from_start_date = Period.objects.get_period_for_date(period_start_date)
        period_from_end_date = Period.objects.get_period_for_date(period_end_date)

        if period_start_date >= period_end_date:
            raise forms.ValidationError('Please check the start date and end date, '
                                        'start date can not be as same or after end date')
        elif period_from_start_date and self.instance.id != period_from_start_date.id:
            raise forms.ValidationError('Please check the start date, it is overlapping with other period')
        elif period_from_end_date and self.instance.id != period_from_start_date.id:
            raise forms.ValidationError('Please check the end date, it is overlapping with other period')

        return period_data