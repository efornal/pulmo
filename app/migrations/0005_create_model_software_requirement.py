# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_objectives_and_targets_connection'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoftwareRequirement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('version', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'software_requirement',
                'verbose_name_plural': 'SoftwareRequirements',
            },
        ),
        migrations.AddField(
            model_name='applicationform',
            name='software_requirements',
            field=models.ManyToManyField(to='app.SoftwareRequirement', blank=True),
        ),
    ]
