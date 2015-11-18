# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_remove_applicationconnectiontarget_ip_firewall'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationconnectionsource',
            name='ip',
            field=models.CharField(max_length=200, null=True, validators=[django.core.validators.validate_ipv46_address]),
        ),
        migrations.AlterField(
            model_name='applicationconnectiontarget',
            name='ip',
            field=models.CharField(max_length=200, null=True, validators=[django.core.validators.validate_ipv46_address]),
        ),
    ]
