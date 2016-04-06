# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_redefined_mandatory_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referrer',
            name='email',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Email', validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='referrer',
            name='phones',
            field=models.CharField(max_length=200, null=True, verbose_name='Tel\xe9fonos', blank=True),
        ),
    ]
