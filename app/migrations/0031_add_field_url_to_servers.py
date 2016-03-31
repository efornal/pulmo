# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_add_field_service_to_connections'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionserver',
            name='url',
            field=models.CharField(max_length=200, null=True, verbose_name='url', blank=True),
        ),
        migrations.AddField(
            model_name='testserver',
            name='url',
            field=models.CharField(max_length=200, null=True, verbose_name='url', blank=True),
        ),
        migrations.AlterField(
            model_name='applicationconnectionsource',
            name='service',
            field=models.CharField(max_length=200, null=True, verbose_name='Servicio', blank=True),
        ),
        migrations.AlterField(
            model_name='applicationconnectiontarget',
            name='service',
            field=models.CharField(max_length=200, null=True, verbose_name='Servicio', blank=True),
        ),
        migrations.AlterField(
            model_name='productionconnectionsource',
            name='service',
            field=models.CharField(max_length=200, null=True, verbose_name='Servicio', blank=True),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='service',
            field=models.CharField(max_length=200, null=True, verbose_name='Servicio', blank=True),
        ),
    ]
