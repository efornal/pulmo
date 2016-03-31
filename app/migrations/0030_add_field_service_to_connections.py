# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_signature_date_without_auto_now_add'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationconnectionsource',
            name='service',
            field=models.CharField(max_length=200, null=True, verbose_name='service', blank=True),
        ),
        migrations.AddField(
            model_name='applicationconnectiontarget',
            name='service',
            field=models.CharField(max_length=200, null=True, verbose_name='service', blank=True),
        ),
        migrations.AddField(
            model_name='productionconnectionsource',
            name='service',
            field=models.CharField(max_length=200, null=True, verbose_name='service', blank=True),
        ),
        migrations.AddField(
            model_name='productionconnectiontarget',
            name='service',
            field=models.CharField(max_length=200, null=True, verbose_name='service', blank=True),
        ),
    ]
