import decimal
import datetime
from django.db import models
from django.db.models import Sum


class PeriodManager(models.Manager):
    def get_period_for_date(self, date):
        try:
            period = self.filter(start_date__lte=date, end_date__gte=date)[0]
        except IndexError:
            period = None
        return period

    def get_period_list_sliced(self, index_number, page_number):
        return self.all()[index_number:page_number]


class Period(models.Model):
    # The period that will contain the expected total amount of expenses
    start_date = models.DateField(default=datetime.datetime.now())
    end_date = models.DateField(default=datetime.datetime.now())
    amount = models.DecimalField(max_digits=8, decimal_places=3)
    description = models.CharField(max_length=200)
    objects = PeriodManager()

    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ['start_date']

    @property
    def get_expense_total(self):
        return Expense.objects.filter(period=self).aggregate(Sum('amount')).get('amount__sum')

    @property
    def remaining_amount(self):
        return self.amount - self.get_expense_total

    @property
    def remaining_percentage(self):
        total = self.get_expense_total
        return (total / self.amount) * decimal.Decimal(100)


class Expense(models.Model):
    # The expense entry against the expected amount for a period
    date = models.DateField(default=datetime.datetime.now())
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=8, decimal_places=3)
    period = models.ForeignKey(Period)

    def __unicode__(self):
        return self.description

    ''' Get the correct period for the expense entry date'''

    def save(self, *args, **kwargs):
        self.period = Period.objects.get_period_for_date(self.date)
        return super(Expense, self).save(*args, **kwargs)

    class Meta:
        ordering = ['period', 'date']

