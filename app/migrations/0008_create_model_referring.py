# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_create_model_scvpermision'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referring',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200, null=True)),
                ('phones', models.CharField(max_length=200, null=True)),
                ('is_applicant', models.BooleanField(default=False)),
                ('application_form', models.ForeignKey(to='app.ApplicationForm')),
            ],
            options={
                'db_table': 'referring',
                'verbose_name_plural': 'Referrings',
            },
        ),
    ]
