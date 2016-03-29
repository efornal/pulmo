# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0026_add_field_user_to_testserver'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionserver',
            name='user',
            field=models.ForeignKey(verbose_name='Usuario', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
