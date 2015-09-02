import decimal
import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

class PeriodList(models.Model):
    """ Priod List will be container for peiords """
    name = models.CharField(max_length=25, verbose_name=_('Name'))
    created_by = models.ForeignKey(User, verbose_name=_('Created By'))
    created_at = models.DateTimeField(auto_now_add=True)

class PeriodManager(models.Manager):
    def get_periods_for_date_and_user(self, date, logged_in_user, period_list):
        """
        Get periods for specific date
        :param date:
        :param logged_in_user:
        :return:
        """
        try:
            period = self.filter(start_date__lte=date,
                                end_date__gte=date,
                                user=logged_in_user,
                                period_list=period_list)
        except IndexError:
            period = None
        return period

    def get_user_period(self, logged_in_user):
        """
        Get user's periods
        :param logged_in_user:
        :return:
        """
        return self.filter(user=logged_in_user)

    def get_today_period(self, logged_in_user):
        """
        Get today's period for the logged in user
        :param logged_in_user:
        :return:
        """
        today = datetime.datetime.utcnow()
        try:
            period = self.get(start_date__lte=today,
                              end_date__gte=today,
                              user=logged_in_user)
        except Period.DoesNotExist:
            period = None
        return period


class Period(models.Model):
    """ The period that will contain the expected total amount of expenses """
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=3)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    period_list = models.ForeignKey(PeriodList, verbose_name=_('Period List'), null=True)
    objects = PeriodManager()

    def __unicode__(self):
        return self.description

    def validate(self):
        period_from_start_date = Period.objects.get_periods_for_date_and_user(self.start_date,
                                                                              self.user,
                                                                              self.period_list)
        period_from_end_date = Period.objects.get_periods_for_date_and_user(self.end_date,
                                                                            self.user,
                                                                            self.period_list)

        if self.pk:
            period_from_start_date = period_from_start_date.exclude(pk=self.pk)
            period_from_end_date = period_from_end_date.exclude(pk=self.pk)

        if self.start_date >= self.end_date:
            raise ValidationError(_('Please check the start date and end date, '
                                    'start date can not be as same or after end date'))
        elif period_from_start_date:
            raise ValidationError(_('Please check the start date, it is overlapping with other period'))
        elif period_from_end_date:
            raise ValidationError(_('Please check the end date, it is overlapping with other period'))

        return True
    def save(self, *args, **kwargs):
        if self.validate():
            return super(Period, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-start_date']

    @property
    def expense_total(self):
        return self.expenses.aggregate(Sum('amount')).get('amount__sum')

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
    """ The expense entry against the expected amount for a period """
    date = models.DateField(default=datetime.datetime.now())
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=8, decimal_places=3)
    period = models.ForeignKey(Period, related_name='expenses')
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        if self.validate():
            self.period = Period.objects.get_periods_for_date_and_user(self.date, self.user)[0]

        return super(Expense, self).save(*args, **kwargs)

    def validate(self):
        period = Period.objects.get_periods_for_date_and_user(self.date, self.user, self.period.period_list)
        if not period:
            raise ValidationError('Please check the date, there is no period in this date.')

    def is_belong_to_user(self, logged_in_user):
        return self.user == logged_in_user

    class Meta:
        ordering = ['period', 'date']
