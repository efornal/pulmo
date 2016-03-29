# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_add_field_user_to_productionserver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionserver',
            name='related_ticket',
            field=models.CharField(max_length=200, null=True, verbose_name='Ticket relacionado', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='related_ticket',
            field=models.CharField(max_length=200, null=True, verbose_name='Ticket relacionado', blank=True),
        ),
    ]
