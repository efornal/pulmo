# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_software_requirements_for_forms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('duration', models.CharField(max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('production_form', models.ForeignKey(to='app.ProductionForm')),
            ],
            options={
                'db_table': 'milestone',
                'verbose_name_plural': 'Milestones',
            },
        ),
    ]
