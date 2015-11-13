# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_software_requirements_restructured'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationConnectionSource',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('ip', models.CharField(max_length=200, null=True)),
                ('observations', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'application_connection_sources',
                'verbose_name_plural': 'ApplicationConnectionSources',
            },
        ),
        migrations.CreateModel(
            name='ApplicationConnectionTarget',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('ip', models.CharField(max_length=200, null=True)),
                ('ip_firewall', models.CharField(max_length=200, null=True)),
                ('observations', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'application_connection_targets',
                'verbose_name_plural': 'ApplicationConnectionTargets',
            },
        ),
        migrations.CreateModel(
            name='ProductionConnectionSource',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('ip', models.CharField(max_length=200, null=True)),
                ('observations', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'production_connection_sources',
                'verbose_name_plural': 'ProductionConnectionSources',
            },
        ),
        migrations.CreateModel(
            name='ProductionConnectionTarget',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('ip', models.CharField(max_length=200, null=True)),
                ('ip_firewall', models.CharField(max_length=200, null=True)),
                ('observations', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'production_connection_targets',
                'verbose_name_plural': 'ProductionConnectionTargets',
            },
        ),
        migrations.RemoveField(
            model_name='applicationform',
            name='connection_sources',
        ),
        migrations.RemoveField(
            model_name='applicationform',
            name='connection_targets',
        ),
        migrations.RemoveField(
            model_name='productionform',
            name='connection_sources',
        ),
        migrations.RemoveField(
            model_name='productionform',
            name='connection_targets',
        ),
        migrations.DeleteModel(
            name='ConnectionSource',
        ),
        migrations.DeleteModel(
            name='ConnectionTarget',
        ),
        migrations.AddField(
            model_name='productionconnectiontarget',
            name='production_form',
            field=models.ForeignKey(to='app.ProductionForm'),
        ),
        migrations.AddField(
            model_name='productionconnectionsource',
            name='production_form',
            field=models.ForeignKey(to='app.ProductionForm'),
        ),
        migrations.AddField(
            model_name='applicationconnectiontarget',
            name='application_form',
            field=models.ForeignKey(to='app.ApplicationForm'),
        ),
        migrations.AddField(
            model_name='applicationconnectionsource',
            name='application_form',
            field=models.ForeignKey(to='app.ApplicationForm'),
        ),
    ]
