# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_translated_model_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationconnectionsource',
            name='application_form',
            field=models.ForeignKey(verbose_name='Formulario de Solicitud', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='applicationconnectionsource',
            name='ip',
            field=models.CharField(max_length=200, null=True, verbose_name='IP', validators=[django.core.validators.validate_ipv46_address]),
        ),
        migrations.AlterField(
            model_name='applicationconnectiontarget',
            name='application_form',
            field=models.ForeignKey(verbose_name='Formulario de Solicitud', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='applicationconnectiontarget',
            name='ip',
            field=models.CharField(max_length=200, null=True, verbose_name='IP', validators=[django.core.validators.validate_ipv46_address]),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creado el'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='proyect',
            field=models.OneToOneField(primary_key=True, serialize=False, to='app.Proyect', verbose_name='Proyecto'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='signature_date',
            field=models.DateTimeField(null=True, verbose_name='fecha de firma', blank=True),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado el'),
        ),
        migrations.AlterField(
            model_name='applicationsoftwarerequirement',
            name='application_form',
            field=models.ForeignKey(verbose_name='Formulario de Solicitud', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='applicationsoftwarerequirement',
            name='version',
            field=models.CharField(max_length=200, null=True, verbose_name='Versi\xf3n'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creado el'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='duration',
            field=models.CharField(max_length=50, null=True, verbose_name='Duraci\xf3n'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='production_form',
            field=models.ForeignKey(verbose_name='Formulario de Producci\xf3n', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='monitoredvariable',
            name='periodicity',
            field=models.CharField(max_length=200, null=True, verbose_name='Periodicidad'),
        ),
        migrations.AlterField(
            model_name='monitoredvariable',
            name='preserving_history_by',
            field=models.CharField(max_length=200, null=True, verbose_name='Preservar historial por'),
        ),
        migrations.AlterField(
            model_name='monitoredvariable',
            name='production_form',
            field=models.ForeignKey(verbose_name='Formulario de Producci\xf3n', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='productionconnectionsource',
            name='ip',
            field=models.CharField(max_length=200, null=True, verbose_name='IP'),
        ),
        migrations.AlterField(
            model_name='productionconnectionsource',
            name='production_form',
            field=models.ForeignKey(verbose_name='Formulario de Producci\xf3n', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='ip',
            field=models.CharField(max_length=200, null=True, verbose_name='IP'),
        ),
        migrations.AlterField(
            model_name='productionconnectiontarget',
            name='production_form',
            field=models.ForeignKey(verbose_name='Formulario de Producci\xf3n', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='applicant',
            field=models.CharField(max_length=200, null=True, verbose_name='Solicitante', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creado el'),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='db_space_after',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio en DB posterior', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='db_space_at_year',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio en DB por a\xf1o', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='db_space_to_start',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio inicial en DB ', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='files_backup',
            field=models.TextField(null=True, verbose_name='Archivos a resguardar', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='fs_space_after',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio en disco posterior', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='fs_space_at_year',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio en disco al a\xf1o', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='fs_space_to_start',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio inicial en disco ', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='minimum_disk_space',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio m\xednimo en disco', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='minimum_memory',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio m\xednimo de memoria', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='minimum_processor',
            field=models.CharField(max_length=200, null=True, verbose_name='Nro m\xednimo de procesadores', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='proyect',
            field=models.OneToOneField(primary_key=True, serialize=False, to='app.Proyect', verbose_name='Proyecto'),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='signature_date',
            field=models.DateTimeField(null=True, verbose_name='fecha de firma', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='suggested_disk_space',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio en disco sugerido', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='suggested_memory',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio de memoria sugerido', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='suggested_processor',
            field=models.CharField(max_length=200, null=True, verbose_name='Nro de procesadores sugeridos', blank=True),
        ),
        migrations.AlterField(
            model_name='productionform',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado el'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='added_backup',
            field=models.BooleanField(default=False, verbose_name='Resguardo a\xf1adido'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='added_monitoring',
            field=models.BooleanField(default=False, verbose_name='Monitoreo a\xf1adido'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='applicant',
            field=models.CharField(max_length=200, null=True, verbose_name='Solicitante', blank=True),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='cluster_virtual_machine',
            field=models.CharField(max_length=200, null=True, verbose_name='Cluster de m\xe1quina virtual'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='database_permissions',
            field=models.CharField(max_length=200, null=True, verbose_name='Permisos en DB'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='database_server',
            field=models.CharField(max_length=200, null=True, verbose_name='Servidor de DB'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='disk_space',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio en disco'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='ip_address',
            field=models.CharField(max_length=200, null=True, verbose_name='Direcci\xf3n IP'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='location_logs',
            field=models.CharField(max_length=200, null=True, verbose_name='Localizaci\xf3n de Logs'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='mac_address',
            field=models.CharField(max_length=200, null=True, verbose_name='Direcci\xf3n MAC'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='processors',
            field=models.CharField(max_length=200, null=True, verbose_name='Procesadores'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='production_form',
            field=models.ForeignKey(verbose_name='Formulario de Producci\xf3n', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='ram_memory',
            field=models.CharField(max_length=200, null=True, verbose_name='Memoria RAM'),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='signature_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='fecha de firma', null=True),
        ),
        migrations.AlterField(
            model_name='productionserver',
            name='virtual_machine_name',
            field=models.CharField(max_length=200, verbose_name='Nombre de m\xe1quina virtual'),
        ),
        migrations.AlterField(
            model_name='productionsoftwarerequirement',
            name='production_form',
            field=models.ForeignKey(verbose_name='Formulario de Producci\xf3n', to='app.ProductionForm'),
        ),
        migrations.AlterField(
            model_name='productionsoftwarerequirement',
            name='version',
            field=models.CharField(max_length=200, null=True, verbose_name='Versi\xf3n'),
        ),
        migrations.AlterField(
            model_name='proyect',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creado el'),
        ),
        migrations.AlterField(
            model_name='proyect',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado el'),
        ),
        migrations.AlterField(
            model_name='referrer',
            name='application_form',
            field=models.ForeignKey(verbose_name='Formulario de Solicitud', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='scvpermission',
            name='application_form',
            field=models.ForeignKey(verbose_name='Formulario de Solicitud', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='applicant',
            field=models.CharField(max_length=200, null=True, verbose_name='Solicitante', blank=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='application_form',
            field=models.ForeignKey(verbose_name='Formulario de Solicitud', to='app.ApplicationForm'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='cluster_virtual_machine',
            field=models.CharField(max_length=200, null=True, verbose_name='Cluster de m\xe1quina virtual'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='database_permissions',
            field=models.CharField(max_length=200, null=True, verbose_name='Permisos en DB'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='database_server',
            field=models.CharField(max_length=200, null=True, verbose_name='Servidor de DB'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='disk_space',
            field=models.CharField(max_length=200, null=True, verbose_name='Espacio en disco'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='ip_address',
            field=models.CharField(max_length=200, null=True, verbose_name='Direcci\xf3n IP'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='location_logs',
            field=models.CharField(max_length=200, null=True, verbose_name='Localizaci\xf3n de Logs'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='mac_address',
            field=models.CharField(max_length=200, null=True, verbose_name='Direcci\xf3n MAC'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='processors',
            field=models.CharField(max_length=200, null=True, verbose_name='Procesadores'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='ram_memory',
            field=models.CharField(max_length=200, null=True, verbose_name='Memoria RAM'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='signature_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='fecha de firma', null=True),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='vcs_repository',
            field=models.CharField(max_length=200, null=True, verbose_name='Repositorio VCS'),
        ),
        migrations.AlterField(
            model_name='testserver',
            name='virtual_machine_name',
            field=models.CharField(max_length=200, verbose_name='Nombre de m\xe1quina virtual'),
        ),
    ]
