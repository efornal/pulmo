# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-22 15:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0053_add_field_user_to_applicationform'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionform',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]
