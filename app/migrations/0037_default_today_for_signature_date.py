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
            model_name='testserver',
            name='signature_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 6, 11, 50, 41, 232292), null=True, verbose_name='fecha de firma', blank=True),
        ),
    ]
