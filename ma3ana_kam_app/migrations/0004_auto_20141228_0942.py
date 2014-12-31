# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ma3ana_kam_app', '0003_auto_20141228_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default=datetime.datetime(2014, 12, 28, 9, 42, 38, 825304)),
            preserve_default=True,
        ),
    ]
