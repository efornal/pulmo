# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_create_model_production_server'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationSoftwareRequirement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('version', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'application_software_requirements',
                'verbose_name_plural': 'ApplicationSoftwareRequirements',
            },
        ),
        migrations.CreateModel(
            name='ProductionSoftwareRequirement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('version', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'production_software_requirements',
                'verbose_name_plural': 'ProductionSoftwareRequirements',
            },
        ),
        migrations.RemoveField(
            model_name='applicationform',
            name='software_requirements',
        ),
        migrations.RemoveField(
            model_name='productionform',
            name='software_requirements',
        ),
        migrations.DeleteModel(
            name='SoftwareRequirement',
        ),
        migrations.AddField(
            model_name='productionsoftwarerequirement',
            name='production_form',
            field=models.ForeignKey(to='app.ProductionForm'),
        ),
        migrations.AddField(
            model_name='applicationsoftwarerequirement',
            name='application_form',
            field=models.ForeignKey(to='app.ApplicationForm'),
        ),
    ]
