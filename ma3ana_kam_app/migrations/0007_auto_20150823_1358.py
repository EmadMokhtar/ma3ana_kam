# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ma3ana_kam_app', '0006_auto_20150823_0257'),
    ]

    operations = [
        migrations.AddField(
            model_name='period',
            name='period_list',
            field=models.ForeignKey(verbose_name='Period List', to='ma3ana_kam_app.PeriodList', null=True),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 8, 23, 13, 58, 33, 636850)),
        ),
    ]
