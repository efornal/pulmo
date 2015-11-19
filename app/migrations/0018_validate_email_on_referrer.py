# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_rename_scvpermision_to_scvpermission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referrer',
            name='email',
            field=models.CharField(max_length=200, null=True, validators=[django.core.validators.EmailValidator()]),
        ),
    ]
