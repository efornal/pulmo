# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_validate_field_ip_on_application_connection'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SCVPermision',
            new_name='SCVPermission',
        ),
        migrations.AlterModelOptions(
            name='scvpermission',
            options={'verbose_name_plural': 'SCVPermissions'},
        ),
        migrations.RenameField(
            model_name='scvpermission',
            old_name='permision',
            new_name='permission',
        ),
        migrations.AlterModelTable(
            name='scvpermission',
            table='scv_permissions',
        ),
    ]
