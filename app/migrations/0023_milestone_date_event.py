# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_changed_observations_by_port'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='date_event',
            field=models.DateTimeField(null=True, verbose_name='date_event', blank=True),
        ),
    ]
