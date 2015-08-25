from django.test import TestCase
from django.contrib.auth.models import User
from django.forms import ValidationError
from ..models import PeriodList, Period
import datetime

class PeriodListTestCases(TestCase):
	""" Testing Period List Business Logic """

	def setUp(self):
		""" Test inital setup """
		self.user = User.objects.create_user('user','user@email.com','password')
		self.period_list, created = PeriodList.objects.get_or_create(name='first_period_list',
			                                                         created_by=self.user)

	def test_create_new_period_list(self):
		""" Tests creating new period list"""
		new_period_list = PeriodList(name='test list', created_by=self.user)
		new_period_list.save()
		self.assertIsInstance(new_period_list, PeriodList)
		self.assertTrue(new_period_list.pk)

	def test_update_period_list(self):
		""" Tests updating period list"""
		period_list_updated_name = 'first period list'
		self.period_list.name = period_list_updated_name
		self.period_list.save()

		self.assertEqual(self.period_list.name, period_list_updated_name)

	def test_delete_period_list(self):
		""" Tests deleting period list"""
		self.period_list.delete()

		self.assertFalse(self.period_list.pk)


class PeriodTestCases(TestCase):
	""" Testing Period Business Logic"""


	def setUp(self):
		""" Test inital setup"""
		self.user = User.objects.create_user('user','user@email.com','password')
		self.period_list, created = PeriodList.objects.get_or_create(name='first_period_list',
			                                                         created_by=self.user)
		self.start_date = datetime.date(2015,1,1)
		self.end_date = datetime.date(2015,2,1)
		self.period, created = Period.objects.get_or_create(start_date=self.start_date,
												   			end_date=self.end_date,
												   			amount=100,
												   			description='test new period',
												   			period_list= self.period_list,
												   			user=self.user)
		

	def test_add_new_period(self):
		""" Tests creating new period"""
		start_date = datetime.date(2015,2,2)
		end_date = datetime.date(2015,3,1)
		new_period = Period(start_date=start_date,
							end_date=end_date,
							amount=100,
							description='test new period',
							period_list= self.period_list,
							user=self.user)
		new_period.save()

		self.assertIsInstance(new_period, Period)
		self.assertTrue(new_period.pk)

	def test_update_period(self):
		""" Test updating period"""
		new_start_date = datetime.date(2015, 1, 2)
		self.period.start_date = new_start_date
		self.period.save()

		self.assertEqual(new_start_date, self.period.start_date)

	def test_creating_period_with_same_start_end_dates_should_fail(self):
		""" Tests insert new period with start & end dates for existing"""
		""" user period in the same list should fail and raise ValidationError"""
		new_period = Period(start_date=self.start_date,
							end_date=self.end_date,
							amount=100,
							description='test new period',
							period_list= self.period_list,
							user=self.user)
		
		self.assertRaises(ValidationError, lambda: new_period.save())

	def test_creating_period_with_same_start_date_should_fail(self):
		""" Tests insert new period with start date for existing"""
		""" user period in the same list should fail and raise ValidationError"""
		end_date = datetime.date(2015,5,1)
		new_period = Period(start_date=self.start_date,
							end_date=end_date,
							amount=100,
							description='test new period',
							period_list= self.period_list,
							user=self.user)
		
		self.assertRaises(ValidationError, lambda: new_period.save())

	def test_creating_period_with_same_end_date_should_fail(self):
		""" Tests insert new period with end date for existing"""
		""" user period in the same list should fail and raise ValidationError"""
		start_date = datetime.date(2014,12,1)
		new_period = Period(start_date=start_date,
							end_date=self.end_date,
							amount=100,
							description='test new period',
							period_list= self.period_list,
							user=self.user)
		
		self.assertRaises(ValidationError, lambda: new_period.save())