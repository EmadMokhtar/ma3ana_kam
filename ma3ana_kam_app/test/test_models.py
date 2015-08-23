from django.test import TestCase
from django.contrib.auth.models import User
from ma3ana_kam_app.models import PeriodList

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
		self.assertTrue(isinstance(new_period_list, PeriodList))
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