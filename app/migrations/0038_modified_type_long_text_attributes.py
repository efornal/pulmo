# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_alter_field_signature_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionserver',
            name='database_permissions',
            field=models.TextField(null=True, verbose_name='Permisos en DB', blank=True),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='location_logs',
            field=models.TextField(null=True, verbose_name='Localizaci\xf3n de Logs', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='database_permissions',
            field=models.TextField(null=True, verbose_name='Permisos en DB', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='location_logs',
            field=models.TextField(null=True, verbose_name='Localizaci\xf3n de Logs', blank=True),
        ),
    ]
