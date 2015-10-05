# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_create_model_monitored_variables'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Referring',
            new_name='Referrer',
        ),
        migrations.AlterModelOptions(
            name='referrer',
            options={'verbose_name_plural': 'Referrers'},
        ),
        migrations.AlterModelTable(
            name='applicationform',
            table='application_forms',
        ),
        migrations.AlterModelTable(
            name='connectionsource',
            table='connection_sources',
        ),
        migrations.AlterModelTable(
            name='connectiontarget',
            table='connection_targets',
        ),
        migrations.AlterModelTable(
            name='milestone',
            table='milestones',
        ),
        migrations.AlterModelTable(
            name='productionform',
            table='production_forms',
        ),
        migrations.AlterModelTable(
            name='referrer',
            table='referrers',
        ),
        migrations.AlterModelTable(
            name='softwarerequirement',
            table='software_requirements',
        ),
    ]
