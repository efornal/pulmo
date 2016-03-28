# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_text_field_port_to_char'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionserver',
            name='related_ticket',
            field=models.CharField(max_length=200, null=True, verbose_name='related_ticket'),
        ),
        migrations.AddField(
            model_name='testserver',
            name='related_ticket',
            field=models.CharField(max_length=200, null=True, verbose_name='related_ticket'),
        ),
    ]
