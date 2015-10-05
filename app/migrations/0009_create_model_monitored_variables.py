# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_create_model_referring'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoredVariable',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('periodicity', models.CharField(max_length=200, null=True)),
                ('preserving_history_by', models.CharField(max_length=200, null=True)),
                ('production_form', models.ForeignKey(to='app.ProductionForm')),
            ],
            options={
                'db_table': 'monitored_variables',
                'verbose_name_plural': 'MonitoredVariables',
            },
        ),
    ]
