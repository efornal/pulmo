# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_proyect'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationForm',
            fields=[
                ('proyect', models.OneToOneField(primary_key=True, serialize=False, to='app.Proyect')),
                ('db_name', models.CharField(max_length=200, null=True, blank=True)),
                ('encoding', models.CharField(max_length=200, null=True, blank=True)),
                ('user_owner', models.CharField(max_length=200, null=True, blank=True)),
                ('user_access', models.CharField(max_length=200, null=True, blank=True)),
                ('observations', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('signature_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'application_form',
                'verbose_name_plural': 'ApplicationForms',
            },
        ),
    ]
