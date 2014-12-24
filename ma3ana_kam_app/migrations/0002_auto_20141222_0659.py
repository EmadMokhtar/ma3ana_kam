# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ma3ana_kam_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'ordering': ['period', 'date']},
        ),
        migrations.AlterModelOptions(
            name='period',
            options={'ordering': ['start_date']},
        ),
        migrations.RenameField(
            model_name='period',
            old_name='Amount',
            new_name='amount',
        ),
        migrations.RenameField(
            model_name='period',
            old_name='Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='period',
            old_name='date_from',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='period',
            old_name='date_to',
            new_name='start_date',
        ),
    ]
