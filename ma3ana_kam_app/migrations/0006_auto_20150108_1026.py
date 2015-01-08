# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ma3ana_kam_app', '0005_auto_20141228_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseAudit',
            fields=[
                ('date', models.DateField(default=datetime.datetime(2015, 1, 8, 10, 26, 14, 260471))),
                ('description', models.CharField(max_length=200)),
                ('amount', models.DecimalField(max_digits=8, decimal_places=3)),
                ('_audit_id', models.AutoField(serialize=False, primary_key=True)),
                ('_audit_timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('_audit_change_type', models.CharField(max_length=1)),
                ('id', models.IntegerField(editable=False, db_index=True)),
                ('period', models.ForeignKey(related_name='_audit_expense', to='ma3ana_kam_app.Period')),
                ('user', models.ForeignKey(related_name='_audit_expense', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-_audit_timestamp'],
                'db_table': 'ma3ana_kam_app_expense_audit',
                'verbose_name_plural': 'expense audit trail',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 1, 8, 10, 26, 14, 260471)),
            preserve_default=True,
        ),
    ]
