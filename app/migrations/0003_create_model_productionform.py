# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_create_model_applicationform'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionForm',
            fields=[
                ('proyect', models.OneToOneField(primary_key=True, serialize=False, to='app.Proyect')),
                ('db_name', models.CharField(max_length=200, null=True, blank=True)),
                ('encoding', models.CharField(max_length=200, null=True, blank=True)),
                ('user_owner', models.CharField(max_length=200, null=True, blank=True)),
                ('user_access', models.CharField(max_length=200, null=True, blank=True)),
                ('db_space_to_start', models.CharField(max_length=200, null=True, blank=True)),
                ('db_space_at_year', models.CharField(max_length=200, null=True, blank=True)),
                ('db_space_after', models.CharField(max_length=200, null=True, blank=True)),
                ('fs_space_to_start', models.CharField(max_length=200, null=True, blank=True)),
                ('fs_space_at_year', models.CharField(max_length=200, null=True, blank=True)),
                ('fs_space_after', models.CharField(max_length=200, null=True, blank=True)),
                ('minimum_memory', models.CharField(max_length=200, null=True, blank=True)),
                ('suggested_memory', models.CharField(max_length=200, null=True, blank=True)),
                ('minimum_disk_space', models.CharField(max_length=200, null=True, blank=True)),
                ('suggested_disk_space', models.CharField(max_length=200, null=True, blank=True)),
                ('minimum_processor', models.CharField(max_length=200, null=True, blank=True)),
                ('suggested_processor', models.CharField(max_length=200, null=True, blank=True)),
                ('files_backup', models.TextField(null=True, blank=True)),
                ('observations', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('applicant', models.CharField(max_length=200, null=True, blank=True)),
                ('signature_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'production_form',
                'verbose_name_plural': 'ProductionForms',
            },
        ),
    ]
