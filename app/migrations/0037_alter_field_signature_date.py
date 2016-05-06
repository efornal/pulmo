# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_ip_not_mandatory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionserver',
            name='signature_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 6, 16, 16, 36, 286435), null=True, verbose_name='fecha de firma', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='signature_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 6, 16, 16, 36, 285236), null=True, verbose_name='fecha de firma', blank=True),
        ),
    ]
