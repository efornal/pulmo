# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_default_today_for_signature_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testserver',
            name='signature_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 6, 15, 42, 21, 683129), null=True, verbose_name='fecha de firma', blank=True),
        ),
    ]
