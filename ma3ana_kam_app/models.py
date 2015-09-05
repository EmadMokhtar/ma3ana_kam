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
    def get_user_periods_for_date(self, date, logged_in_user, period_list):
        """
        Get periods for specific date
        :param date:
        :param logged_in_user:
        :param period_list:
        :return:
        """
        return self.filter(start_date__lte=date,
                           end_date__gte=date,
                           user=logged_in_user,
                           period_list=period_list)


    def get_user_period_for_date(self, date, logged_in_user, period_list):
        """
        Get user's period for specific date
        :param date:
        :param logged_in_user:
        :param period_list:
        :return:
        """
        try:
            period = self.get(start_date__lte=date,
                                end_date__gte=date,
                                user=logged_in_user,
                                period_list=period_list)
        except Period.DoesNotExist:
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
    period_list = models.ForeignKey(PeriodList,
                                    verbose_name=_('Period List'),
                                    null=True)
    objects = PeriodManager()

    def __unicode__(self):
        return self.description

    def is_start_date_invalid(self):
        """
        Check if period's start date are overlapping with another
        period in the same period list
        """
        return Period.objects.filter(user=self.user,
                              period_list=self.period_list,
                              start_date__lte=self.start_date,
                              end_date__gte=self.start_date).exclude(pk=self.pk).exists()

    def is_end_date_invalid(self):
        """
        Check if period's start date are overlapping with another
        period in the same period list
        """
        return Period.objects.filter(user=self.user,
                                     period_list=self.period_list,
                                     start_date__lte=self.end_date,
                                     end_date__gte=self.end_date).exclude(pk=self.pk).exists()

    def validate(self):
        """
        Validate period's start and end dates:
        1- Start date are earlier that enda date.
        2- Start date not over lapping with other period in the period list.
        3- End date not over lapping with other period in the period list.
        """
        if self.start_date >= self.end_date:
            raise ValidationError(_('Please check the start date and end date, '
                                    'start date can not be as same or after end date'))
        elif self.is_start_date_invalid():
            raise ValidationError(_('Please check the start date, it is overlapping with other period'))
        elif self.is_end_date_invalid():
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

    @property
    def expenses(self):
        return self.objects.expenses


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
        period = Period.objects.get_user_period_for_date(self.date,
                                                         self.user,
                                                         self.period.period_list)
        if not period:
            raise ValidationError('Please check the date, there is no period in this date.')
        self.period = period
        return super(Expense, self).save(*args, **kwargs)

    def is_belong_to_user(self, logged_in_user):
        return self.user == logged_in_user

    class Meta:
        ordering = ['period', 'date']
