# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_create_model_testserver'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionServer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('virtual_machine_name', models.CharField(max_length=200)),
                ('ip_address', models.CharField(max_length=200, null=True)),
                ('mac_address', models.CharField(max_length=200, null=True)),
                ('ram_memory', models.CharField(max_length=200, null=True)),
                ('disk_space', models.CharField(max_length=200, null=True)),
                ('processors', models.CharField(max_length=200, null=True)),
                ('database_permissions', models.CharField(max_length=200, null=True)),
                ('database_server', models.CharField(max_length=200, null=True)),
                ('location_logs', models.CharField(max_length=200, null=True)),
                ('cluster_virtual_machine', models.CharField(max_length=200, null=True)),
                ('observations', models.TextField(null=True, blank=True)),
                ('added_monitoring', models.BooleanField(default=False)),
                ('added_backup', models.BooleanField(default=False)),
                ('applicant', models.CharField(max_length=200, null=True, blank=True)),
                ('signature_date', models.DateTimeField(null=True, blank=True)),
                ('production_form', models.ForeignKey(to='app.ProductionForm')),
            ],
            options={
                'db_table': 'production_servers',
                'verbose_name_plural': 'ProductionServers',
            },
        ),
        migrations.AlterModelOptions(
            name='testserver',
            options={'verbose_name_plural': 'TestServers'},
        ),
    ]
