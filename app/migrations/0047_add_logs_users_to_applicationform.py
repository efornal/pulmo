# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-05 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_applicationform_extra_database_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationform',
            name='logs_users',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='logs_users'),
        ),
        migrations.AddField(
            model_name='applicationform',
            name='logs_visualization',
            field=models.IntegerField(default=1, verbose_name='logs_visualization'),
        ),
    ]
