# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_related_ticket_permit_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionserver',
            name='signature_date',
            field=models.DateTimeField(null=True, verbose_name='fecha de firma', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='signature_date',
            field=models.DateTimeField(null=True, verbose_name='fecha de firma', blank=True),
        ),
    ]
