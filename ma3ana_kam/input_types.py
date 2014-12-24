from django import forms


class DateTypeInput(forms.widgets.TextInput):
    input_type = 'date'