# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-25 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_productionform_related_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionserver',
            name='added_backup',
            field=models.BooleanField(default=False, verbose_name='Resguardo MySQL'),
        ),
    ]
