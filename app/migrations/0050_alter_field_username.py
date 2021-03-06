# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-21 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_add_field_username_to_sources_and_targets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationconnectionsource',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='applicationconnectiontarget',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='productionconnectionsource',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Usuario'),
        ),
    ]
