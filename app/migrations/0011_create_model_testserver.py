# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_pluralized_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestServer',
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
                ('vcs_repository', models.CharField(max_length=200, null=True)),
                ('observations', models.TextField(null=True, blank=True)),
                ('applicant', models.CharField(max_length=200, null=True, blank=True)),
                ('signature_date', models.DateTimeField(null=True, blank=True)),
                ('application_form', models.ForeignKey(to='app.ApplicationForm')),
            ],
            options={
                'db_table': 'test_servers',
                'verbose_name_plural': 'test_servers',
            },
        ),
    ]
