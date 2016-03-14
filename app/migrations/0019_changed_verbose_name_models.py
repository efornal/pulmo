# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_validate_email_on_referrer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicationconnectionsource',
            options={'verbose_name': 'ApplicationConnectionSource', 'verbose_name_plural': 'ApplicationConnectionSources'},
        ),
        migrations.AlterModelOptions(
            name='applicationconnectiontarget',
            options={'verbose_name': 'ApplicationConnectionTarget', 'verbose_name_plural': 'ApplicationConnectionTargets'},
        ),
        migrations.AlterModelOptions(
            name='applicationform',
            options={'verbose_name': 'ApplicationForm', 'verbose_name_plural': 'ApplicationForms'},
        ),
        migrations.AlterModelOptions(
            name='applicationsoftwarerequirement',
            options={'verbose_name': 'ApplicationSoftwareRequirement', 'verbose_name_plural': 'ApplicationSoftwareRequirements'},
        ),
        migrations.AlterModelOptions(
            name='milestone',
            options={'verbose_name': 'Milestone', 'verbose_name_plural': 'Milestones'},
        ),
        migrations.AlterModelOptions(
            name='monitoredvariable',
            options={'verbose_name': 'MonitoredVariable', 'verbose_name_plural': 'MonitoredVariables'},
        ),
        migrations.AlterModelOptions(
            name='productionconnectionsource',
            options={'verbose_name': 'ProductionConnectionSource', 'verbose_name_plural': 'ProductionConnectionSources'},
        ),
        migrations.AlterModelOptions(
            name='productionconnectiontarget',
            options={'verbose_name': 'ProductionConnectionTarget', 'verbose_name_plural': 'ProductionConnectionTargets'},
        ),
        migrations.AlterModelOptions(
            name='productionform',
            options={'verbose_name': 'ProductionForm', 'verbose_name_plural': 'ProductionForms'},
        ),
        migrations.AlterModelOptions(
            name='productionserver',
            options={'verbose_name': 'ProductionServer', 'verbose_name_plural': 'ProductionServers'},
        ),
        migrations.AlterModelOptions(
            name='productionsoftwarerequirement',
            options={'verbose_name': 'ProductionSoftwareRequirement', 'verbose_name_plural': 'ProductionSoftwareRequirements'},
        ),
        migrations.AlterModelOptions(
            name='proyect',
            options={'verbose_name': 'Proyect', 'verbose_name_plural': 'Proyects'},
        ),
        migrations.AlterModelOptions(
            name='referrer',
            options={'verbose_name': 'Referrer', 'verbose_name_plural': 'Referrers'},
        ),
        migrations.AlterModelOptions(
            name='scvpermission',
            options={'verbose_name': 'SCVPermission', 'verbose_name_plural': 'SCVPermissions'},
        ),
        migrations.AlterModelOptions(
            name='testserver',
            options={'verbose_name': 'TestServer', 'verbose_name_plural': 'TestServers'},
        ),
    ]
