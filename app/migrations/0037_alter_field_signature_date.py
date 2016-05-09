# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_ip_not_mandatory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionserver',
            name='signature_date',
            field=models.DateTimeField(auto_now=True, verbose_name='fecha de firma', null=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='signature_date',
            field=models.DateTimeField(auto_now=True, verbose_name='fecha de firma', null=True),
        ),
    ]
