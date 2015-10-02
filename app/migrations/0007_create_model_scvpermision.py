# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_create_model_milestone'),
    ]

    operations = [
        migrations.CreateModel(
            name='SCVPermision',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('user', models.CharField(max_length=200)),
                ('permision', models.CharField(max_length=50)),
                ('application_form', models.ForeignKey(to='app.ApplicationForm')),
            ],
            options={
                'db_table': 'scv_permisions',
                'verbose_name_plural': 'SCVPermisions',
            },
        ),
    ]
