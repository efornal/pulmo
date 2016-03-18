# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_now_for_signature_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productionconnectiontarget',
            name='observations',
        ),
        migrations.AddField(
            model_name='productionconnectiontarget',
            name='port',
            field=models.TextField(null=True, verbose_name='port', blank=True),
        ),
    ]
