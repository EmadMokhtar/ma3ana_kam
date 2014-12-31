from django.contrib import admin
from ma3ana_kam_app.models import Expense, Period


class PeriodAdmin(admin.ModelAdmin):
    list_display = ('description', 'start_date', 'end_date', 'amount')
    search_fields = ('start_date', 'end_date', 'description')


admin.site.register(Expense)
admin.site.register(Period, PeriodAdmin)