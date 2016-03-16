# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_changed_verbose_name_models'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicationconnectionsource',
            options={'verbose_name': 'Fuente de conexi\xf3n de solicitud', 'verbose_name_plural': 'Fuentes de conexi\xf3n de solicitud'},
        ),
        migrations.AlterModelOptions(
            name='applicationconnectiontarget',
            options={'verbose_name': 'Destino de conexi\xf3n de solicitud', 'verbose_name_plural': 'Destinos de conexi\xf3n de solicitud'},
        ),
        migrations.AlterModelOptions(
            name='applicationform',
            options={'verbose_name': 'Formulario de Solicitud', 'verbose_name_plural': 'Formularios de Solicitud'},
        ),
        migrations.AlterModelOptions(
            name='applicationsoftwarerequirement',
            options={'verbose_name': 'Requerimiento de software de solicitud', 'verbose_name_plural': 'Requerimientos de software de solicitud'},
        ),
        migrations.AlterModelOptions(
            name='milestone',
            options={'verbose_name': 'Hito', 'verbose_name_plural': 'Hitos'},
        ),
        migrations.AlterModelOptions(
            name='monitoredvariable',
            options={'verbose_name': 'Variable monitoreada', 'verbose_name_plural': 'Variables monitoreadas'},
        ),
        migrations.AlterModelOptions(
            name='productionconnectionsource',
            options={'verbose_name': 'Fuente de conexi\xf3n de producci\xf3n', 'verbose_name_plural': 'Fuentes de conexi\xf3n de producci\xf3n'},
        ),
        migrations.AlterModelOptions(
            name='productionconnectiontarget',
            options={'verbose_name': 'Destino de conexi\xf3n de producci\xf3n', 'verbose_name_plural': 'Destinos de conexi\xf3n de producci\xf3n'},
        ),
        migrations.AlterModelOptions(
            name='productionform',
            options={'verbose_name': 'Formulario de Producci\xf3n', 'verbose_name_plural': 'Formularios de Producci\xf3n'},
        ),
        migrations.AlterModelOptions(
            name='productionserver',
            options={'verbose_name': 'Servidor de Producci\xf3n', 'verbose_name_plural': 'Servidores de Producci\xf3n'},
        ),
        migrations.AlterModelOptions(
            name='productionsoftwarerequirement',
            options={'verbose_name': 'Requerimiento de software de producci\xf3n', 'verbose_name_plural': 'Requerimientos de software de producci\xf3n'},
        ),
        migrations.AlterModelOptions(
            name='proyect',
            options={'verbose_name': 'Proyecto', 'verbose_name_plural': 'Proyectos'},
        ),
        migrations.AlterModelOptions(
            name='referrer',
            options={'verbose_name': 'Referente', 'verbose_name_plural': 'Referentes'},
        ),
        migrations.AlterModelOptions(
            name='scvpermission',
            options={'verbose_name': 'Permiso SCV', 'verbose_name_plural': 'Permisos SCV'},
        ),
        migrations.AlterModelOptions(
            name='testserver',
            options={'verbose_name': 'Servidor de Test', 'verbose_name_plural': 'Servidores de Test'},
        ),
        migrations.AlterField(
            model_name='applicationconnectionsource',
            name='application_form',
            field=models.ForeignKey(verbose_name='application_form', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='applicationconnectionsource',
            name='ip',
            field=models.CharField(max_length=200, null=True, verbose_name='ip', validators=[django.core.validators.validate_ipv46_address]),
        ),
        migrations.AlterField(
            model_name='applicationconnectionsource',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='applicationconnectionsource',
            name='observations',
            field=models.TextField(null=True, verbose_name='Observaciones', blank=True),
        ),
        migrations.AlterField(
            model_name='applicationconnectiontarget',
            name='application_form',
            field=models.ForeignKey(verbose_name='application_form', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='applicationconnectiontarget',
            name='ip',
            field=models.CharField(max_length=200, null=True, verbose_name='ip', validators=[django.core.validators.validate_ipv46_address]),
        ),
        migrations.AlterField(
            model_name='applicationconnectiontarget',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='applicationconnectiontarget',
            name='observations',
            field=models.TextField(null=True, verbose_name='Observaciones', blank=True),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='db_name',
            field=models.CharField(max_length=200, null=True, verbose_name='Nombre DB', blank=True),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='encoding',
            field=models.CharField(max_length=200, null=True, verbose_name='Codificaci\xf3n', blank=True),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='observations',
            field=models.TextField(null=True, verbose_name='Observaciones', blank=True),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='proyect',
            field=models.OneToOneField(primary_key=True, serialize=False, to='app.Proyect', verbose_name='proyect'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='signature_date',
            field=models.DateTimeField(null=True, verbose_name='signature_date', blank=True),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated_at'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='user_access',
            field=models.CharField(max_length=200, null=True, verbose_name='Usuario acceso', blank=True),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='user_owner',
            field=models.CharField(max_length=200, null=True, verbose_name='Usuario owner', blank=True),
        ),
        migrations.AlterField(
            model_name='applicationsoftwarerequirement',
            name='application_form',
            field=models.ForeignKey(verbose_name='application_form', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='applicationsoftwarerequirement',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='applicationsoftwarerequirement',
            name='version',
            field=models.CharField(max_length=200, null=True, verbose_name='version'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='description',
            field=models.CharField(max_length=200, verbose_name='Descripci\xf3n'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='duration',
            field=models.CharField(max_length=50, null=True, verbose_name='duration'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='production_form',
            field=models.ForeignKey(verbose_name='production_form', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='monitoredvariable',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='monitoredvariable',
            name='periodicity',
            field=models.CharField(max_length=200, null=True, verbose_name='periodicity'),
        ),
        migrations.AlterField(
            model_name='monitoredvariable',
            name='preserving_history_by',
            field=models.CharField(max_length=200, null=True, verbose_name='preserving_history_by'),
        ),
        migrations.AlterField(
            model_name='monitoredvariable',
            name='production_form',
            field=models.ForeignKey(verbose_name='production_form', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='productionconnectionsource',
            name='ip',
            field=models.CharField(max_length=200, null=True, verbose_name='ip'),
        ),
        migrations.AlterField(
            model_name='productionconnectionsource',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='productionconnectionsource',
            name='observations',
            field=models.TextField(null=True, verbose_name='Observaciones', blank=True),
        ),
        migrations.AlterField(
            model_name='productionconnectionsource',
            name='production_form',
            field=models.ForeignKey(verbose_name='production_form', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='ip',
            field=models.CharField(max_length=200, null=True, verbose_name='ip'),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='ip_firewall',
            field=models.CharField(max_length=200, null=True, verbose_name='ip_firewall'),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='observations',
            field=models.TextField(null=True, verbose_name='Observaciones', blank=True),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='production_form',
            field=models.ForeignKey(verbose_name='production_form', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='applicant',
            field=models.CharField(max_length=200, null=True, verbose_name='applicant', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='db_name',
            field=models.CharField(max_length=200, null=True, verbose_name='Nombre DB', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='db_space_after',
            field=models.CharField(max_length=200, null=True, verbose_name='db_space_after', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='db_space_at_year',
            field=models.CharField(max_length=200, null=True, verbose_name='db_space_at_year', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='db_space_to_start',
            field=models.CharField(max_length=200, null=True, verbose_name='db_space_to_start', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='encoding',
            field=models.CharField(max_length=200, null=True, verbose_name='Codificaci\xf3n', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='files_backup',
            field=models.TextField(null=True, verbose_name='files_backup', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='fs_space_after',
            field=models.CharField(max_length=200, null=True, verbose_name='fs_space_after', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='fs_space_at_year',
            field=models.CharField(max_length=200, null=True, verbose_name='fs_space_at_year', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='fs_space_to_start',
            field=models.CharField(max_length=200, null=True, verbose_name='fs_space_to_start', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='minimum_disk_space',
            field=models.CharField(max_length=200, null=True, verbose_name='minimum_disk_space', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='minimum_memory',
            field=models.CharField(max_length=200, null=True, verbose_name='minimum_memory', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='minimum_processor',
            field=models.CharField(max_length=200, null=True, verbose_name='minimum_processor', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='observations',
            field=models.TextField(null=True, verbose_name='Observaciones', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='proyect',
            field=models.OneToOneField(primary_key=True, serialize=False, to='app.Proyect', verbose_name='proyect'),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='signature_date',
            field=models.DateTimeField(null=True, verbose_name='signature_date', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='suggested_disk_space',
            field=models.CharField(max_length=200, null=True, verbose_name='suggested_disk_space', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='suggested_memory',
            field=models.CharField(max_length=200, null=True, verbose_name='suggested_memory', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='suggested_processor',
            field=models.CharField(max_length=200, null=True, verbose_name='suggested_processor', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated_at'),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='user_access',
            field=models.CharField(max_length=200, null=True, verbose_name='Usuario acceso', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='user_owner',
            field=models.CharField(max_length=200, null=True, verbose_name='Usuario owner', blank=True),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='added_backup',
            field=models.BooleanField(default=False, verbose_name='added_backup'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='added_monitoring',
            field=models.BooleanField(default=False, verbose_name='added_monitoring'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='applicant',
            field=models.CharField(max_length=200, null=True, verbose_name='applicant', blank=True),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='cluster_virtual_machine',
            field=models.CharField(max_length=200, null=True, verbose_name='cluster_virtual_machine'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='database_permissions',
            field=models.CharField(max_length=200, null=True, verbose_name='database_permissions'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='database_server',
            field=models.CharField(max_length=200, null=True, verbose_name='database_server'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='disk_space',
            field=models.CharField(max_length=200, null=True, verbose_name='disk_space'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='ip_address',
            field=models.CharField(max_length=200, null=True, verbose_name='ip_address'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='location_logs',
            field=models.CharField(max_length=200, null=True, verbose_name='location_logs'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='mac_address',
            field=models.CharField(max_length=200, null=True, verbose_name='mac_address'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='observations',
            field=models.TextField(null=True, verbose_name='Observaciones', blank=True),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='processors',
            field=models.CharField(max_length=200, null=True, verbose_name='processors'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='production_form',
            field=models.ForeignKey(verbose_name='production_form', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='ram_memory',
            field=models.CharField(max_length=200, null=True, verbose_name='ram_memory'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='signature_date',
            field=models.DateTimeField(null=True, verbose_name='signature_date', blank=True),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='virtual_machine_name',
            field=models.CharField(max_length=200, verbose_name='virtual_machine_name'),
        ),
        migrations.AlterField(
            model_name='productionsoftwarerequirement',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='productionsoftwarerequirement',
            name='production_form',
            field=models.ForeignKey(verbose_name='production_form', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='productionsoftwarerequirement',
            name='version',
            field=models.CharField(max_length=200, null=True, verbose_name='version'),
        ),
        migrations.AlterField(
            model_name='proyect',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='proyect',
            name='description',
            field=models.TextField(null=True, verbose_name='Descripci\xf3n', blank=True),
        ),
        migrations.AlterField(
            model_name='proyect',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='proyect',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated_at'),
        ),
        migrations.AlterField(
            model_name='referrer',
            name='application_form',
            field=models.ForeignKey(verbose_name='application_form', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='referrer',
            name='email',
            field=models.CharField(max_length=200, null=True, verbose_name='Email', validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='referrer',
            name='is_applicant',
            field=models.BooleanField(default=False, verbose_name='Es solicitante'),
        ),
        migrations.AlterField(
            model_name='referrer',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='referrer',
            name='phones',
            field=models.CharField(max_length=200, null=True, verbose_name='Tel\xe9fonos'),
        ),
        migrations.AlterField(
            model_name='scvpermission',
            name='application_form',
            field=models.ForeignKey(verbose_name='application_form', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='scvpermission',
            name='permission',
            field=models.CharField(max_length=50, verbose_name='Permiso'),
        ),
        migrations.AlterField(
            model_name='scvpermission',
            name='user',
            field=models.CharField(max_length=200, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='applicant',
            field=models.CharField(max_length=200, null=True, verbose_name='applicant', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='application_form',
            field=models.ForeignKey(verbose_name='application_form', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='cluster_virtual_machine',
            field=models.CharField(max_length=200, null=True, verbose_name='cluster_virtual_machine'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='database_permissions',
            field=models.CharField(max_length=200, null=True, verbose_name='database_permissions'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='database_server',
            field=models.CharField(max_length=200, null=True, verbose_name='database_server'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='disk_space',
            field=models.CharField(max_length=200, null=True, verbose_name='disk_space'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='ip_address',
            field=models.CharField(max_length=200, null=True, verbose_name='ip_address'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='location_logs',
            field=models.CharField(max_length=200, null=True, verbose_name='location_logs'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='mac_address',
            field=models.CharField(max_length=200, null=True, verbose_name='mac_address'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='observations',
            field=models.TextField(null=True, verbose_name='Observaciones', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='processors',
            field=models.CharField(max_length=200, null=True, verbose_name='processors'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='ram_memory',
            field=models.CharField(max_length=200, null=True, verbose_name='ram_memory'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='signature_date',
            field=models.DateTimeField(null=True, verbose_name='signature_date', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='vcs_repository',
            field=models.CharField(max_length=200, null=True, verbose_name='vcs_repository'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='virtual_machine_name',
            field=models.CharField(max_length=200, verbose_name='virtual_machine_name'),
        ),
    ]
