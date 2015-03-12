import decimal
import datetime
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _


class PeriodManager(models.Manager):
    def get_period_for_date(self, date, logged_in_user):
        try:
            period = self.filter(start_date__lte=date, end_date__gte=date, user=logged_in_user)

        except IndexError:
            period = None
        return period

    def get_period_for_user(self, logged_in_user):
        return self.filter(user=logged_in_user)


class Period(models.Model):
    # The period that will contain the expected total amount of expenses
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=3)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    objects = PeriodManager()

    def __unicode__(self):
        return self.description

    def validate(self):
        period_from_start_date = Period.objects.get_period_for_date(self.start_date, self.user)
        period_from_end_date = Period.objects.get_period_for_date(self.end_date, self.user)

        if self.id:
            period_from_start_date = Period.objects.get_period_for_date(self.start_date, self.user).exclude(pk=self.id)
            period_from_end_date = Period.objects.get_period_for_date(self.end_date, self.user).exclude(pk=self.id)
        else:
            period_from_start_date = Period.objects.get_period_for_date(self.start_date, self.user)
            period_from_end_date = Period.objects.get_period_for_date(self.end_date, self.user)

        if self.start_date >= self.end_date:
            raise ValidationError(_('Please check the start date and end date, '
                                  'start date can not be as same or after end date'))
        elif period_from_start_date:
            raise ValidationError(_('Please check the start date, it is overlapping with other period'))
        elif period_from_end_date:
            raise ValidationError(_('Please check the end date, it is overlapping with other period'))

    def save(self, *args, **kwargs):

        self.validate()
        super(Period, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-start_date']

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

    def is_belong_to_user(self, logged_in_user):
        return self.user == logged_in_user


class Expense(models.Model):
    # The expense entry against the expected amount for a period
    date = models.DateField(default=datetime.datetime.now())
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=8, decimal_places=3)
    period = models.ForeignKey(Period)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.description

    '''Get the correct period for the expense entry date'''
    def save(self, *args, **kwargs):
        self.validate()
        self.period = Period.objects.get_period_for_date(self.date, self.user)[0]

        return super(Expense, self).save(*args, **kwargs)

    def validate(self):
        period = Period.objects.get_period_for_date(self.date, self.user)
        if not period:
            raise ValidationError('Please check the date, there is no period in this date.')

    def is_belong_to_user(self, logged_in_user):
        return self.user == logged_in_user

    class Meta:
        ordering = ['period', 'date']