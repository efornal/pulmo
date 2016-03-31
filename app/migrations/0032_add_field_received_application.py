# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_add_field_url_to_servers'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationform',
            name='received_application',
            field=models.BooleanField(default=False, verbose_name='received_application'),
        ),
        migrations.AddField(
            model_name='productionform',
            name='received_application',
            field=models.BooleanField(default=False, verbose_name='received_application'),
        ),
    ]
