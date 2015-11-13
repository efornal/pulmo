# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_origin_connections_restructured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationconnectiontarget',
            name='ip_firewall',
        ),
    ]
