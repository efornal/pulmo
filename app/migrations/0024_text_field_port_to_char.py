# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_milestone_date_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='port',
            field=models.CharField(max_length=200, null=True, verbose_name='port', blank=True),
        ),
    ]
