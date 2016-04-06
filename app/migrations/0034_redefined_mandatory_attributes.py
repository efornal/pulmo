# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_alter_field_received_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionserver',
            name='database_permissions',
            field=models.CharField(max_length=200, null=True, verbose_name='Permisos en DB', blank=True),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='location_logs',
            field=models.CharField(max_length=200, null=True, verbose_name='Localizaci\xf3n de Logs', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='database_permissions',
            field=models.CharField(max_length=200, null=True, verbose_name='Permisos en DB', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='ip_address',
            field=models.CharField(max_length=200, null=True, verbose_name='Direcci\xf3n IP', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='location_logs',
            field=models.CharField(max_length=200, null=True, verbose_name='Localizaci\xf3n de Logs', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='vcs_repository',
            field=models.CharField(max_length=200, null=True, verbose_name='Repositorio VCS', blank=True),
        ),
    ]
