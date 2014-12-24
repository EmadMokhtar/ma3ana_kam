# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=200)),
                ('amount', models.DecimalField(max_digits=8, decimal_places=3)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('Amount', models.DecimalField(max_digits=8, decimal_places=3)),
                ('Description', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='expense',
            name='period',
            field=models.ForeignKey(to='ma3ana_kam_app.Period'),
            preserve_default=True,
        ),
    ]
