# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_add_field_received_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationform',
            name='received_application',
            field=models.BooleanField(default=False, verbose_name='Solicitud recibida'),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='received_application',
            field=models.BooleanField(default=False, verbose_name='Solicitud recibida'),
        ),
    ]
