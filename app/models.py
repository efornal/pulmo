# -*- encoding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils.translation import ugettext as _
from django.core.validators import validate_ipv46_address, validate_email
from django.contrib.auth.models import User
    
class Proyect(models.Model):
    id = models.AutoField( primary_key=True,null=False)
    name = models.CharField( max_length=200,null=False,verbose_name=_('name'))
    description = models.TextField( null=True, blank=True,verbose_name=_('description'))
    created_at = models.DateTimeField( auto_now_add=True,verbose_name=_('created_at'))
    updated_at = models.DateTimeField( auto_now=True,verbose_name=_('updated_at'))
    
    class Meta:
        db_table = 'proyects'
        verbose_name = _('Proyect')
        verbose_name_plural = _('Proyects')

    def __unicode__(self):
        return "%s" % (self.name)

    @classmethod
    def without_test_server(cls):
        return Proyect.objects \
                      .filter(applicationform__testserver__application_form__isnull=False) \
                      .order_by('name')

    
class ApplicationForm (models.Model):
    proyect = models.OneToOneField(Proyect, primary_key=True,verbose_name=_('proyect'))

    db_name = models.CharField(max_length=200, null=True, blank=True,verbose_name=_('db_name'))
    encoding = models.CharField(max_length=200, null=True, blank=True,verbose_name=_('encoding'))
    user_owner = models.CharField(max_length=200, null=True, blank=True,verbose_name=_('user_owner'))
    user_access = models.CharField(max_length=200, null=True, blank=True,verbose_name=_('user_access'))

    observations = models.TextField( null=True, blank=True,verbose_name=_('observations'))

    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True,verbose_name=_('updated_at'))
    signature_date = models.DateTimeField(null=True, blank=True,verbose_name=_('signature_date'))

    class Meta:
        db_table = 'application_forms'
        verbose_name = _('ApplicationForm')
        verbose_name_plural = _('ApplicationForms')

    def __unicode__(self):
        return "%s" % (self.proyect.name)

    
class ProductionForm (models.Model):
    proyect = models.OneToOneField(Proyect, primary_key=True,verbose_name=_('proyect'))

    db_name = models.CharField(max_length=200, null=True, blank=True,verbose_name=_('db_name'))
    encoding = models.CharField(max_length=200, null=True, blank=True,verbose_name=_('encoding'))
    user_owner = models.CharField(max_length=200, null=True, blank=True,verbose_name=_('user_owner'))
    user_access = models.CharField(max_length=200, null=True, blank=True,verbose_name=_('user_access'))

    db_space_to_start = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('db_space_to_start'))
    db_space_at_year  = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('db_space_at_year'))
    db_space_after    = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('db_space_after'))
    fs_space_to_start = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('fs_space_to_start'))
    fs_space_at_year  = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('fs_space_at_year'))
    fs_space_after    = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('fs_space_after'))

    minimum_memory = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('minimum_memory'))
    minimum_disk_space = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('minimum_disk_space'))
    minimum_processor = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('minimum_processor'))

    suggested_memory = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('suggested_memory'))
    suggested_disk_space = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('suggested_disk_space'))
    suggested_processor = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('suggested_processor'))

    files_backup = models.TextField( null=True, blank=True,
                                         verbose_name=_('files_backup'))
    observations = models.TextField( null=True, blank=True,
                                         verbose_name=_('observations'))

    created_at = models.DateTimeField(auto_now_add=True,
                                         verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True,
                                         verbose_name=_('updated_at'))

    applicant = models.CharField(max_length=200, null=True, blank=True,
                                         verbose_name=_('applicant'))
    signature_date = models.DateTimeField(null=True, blank=True,
                                         verbose_name=_('signature_date'))

    class Meta:
        db_table = 'production_forms'
        verbose_name = _('ProductionForm')
        verbose_name_plural = _('ProductionForms')

    def __unicode__(self):
        return "%s" % (self.proyect.name)


class ApplicationConnectionSource(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False,
                                         verbose_name=_('name'))
    ip = models.CharField(max_length=200, null=True,
                          verbose_name=_('ip'),
                          validators=[validate_ipv46_address])
    observations = models.TextField(null=True, blank=True,
                                    verbose_name=_('observations'))
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False,
                                         verbose_name=_('application_form'))
    
    class Meta:
        db_table = 'application_connection_sources'
        verbose_name = _('ApplicationConnectionSource')
        verbose_name_plural = _('ApplicationConnectionSources')

    def __unicode__(self):
        return "%s" % (self.name)

    
class ProductionConnectionSource(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False,verbose_name=_('name'))
    ip = models.CharField(max_length=200,null=True,verbose_name=_('ip'))
    observations = models.TextField(null=True, blank=True,verbose_name=_('observations'))
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False,
                                        verbose_name=_('production_form'))
    
    class Meta:
        db_table = 'production_connection_sources'
        verbose_name = _('ProductionConnectionSource')
        verbose_name_plural = _('ProductionConnectionSources')

    def __unicode__(self):
        return "%s" % (self.name)

    
class ApplicationConnectionTarget(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False,verbose_name=_('name'))
    ip = models.CharField(max_length=200,null=True,verbose_name=_('ip'),
                          validators=[validate_ipv46_address])
    observations = models.TextField(null=True, blank=True,verbose_name=_('observations'))
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False,
                                         verbose_name=_('application_form'))
    
    class Meta:
        db_table = 'application_connection_targets'
        verbose_name = _('ApplicationConnectionTarget')
        verbose_name_plural = _('ApplicationConnectionTargets')

    def __unicode__(self):
        return "%s" % (self.name)

class ProductionConnectionTarget(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False,verbose_name=_('name'))
    ip = models.CharField(max_length=200,null=True,verbose_name=_('ip'))
    ip_firewall  = models.CharField(max_length=200,null=True,verbose_name=_('ip_firewall'))
    port = models.CharField(max_length=200, null=True, blank=True,verbose_name=_('port'))
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False,
                                        verbose_name=_('production_form'))
        
    class Meta:
        db_table = 'production_connection_targets'
        verbose_name = _('ProductionConnectionTarget')
        verbose_name_plural = _('ProductionConnectionTargets')

    def __unicode__(self):
        return "%s" % (self.name)

    
class ApplicationSoftwareRequirement(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False,verbose_name=_('name'))
    version = models.CharField(max_length=200,null=True,verbose_name=_('version'))
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False,
                                         verbose_name=_('application_form'))
    
    class Meta:
        db_table = 'application_software_requirements'
        verbose_name = _('ApplicationSoftwareRequirement')
        verbose_name_plural = _('ApplicationSoftwareRequirements')

    def __unicode__(self):
        return "%s" % (self.name)

    
class ProductionSoftwareRequirement(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False,verbose_name=_('name'))
    version = models.CharField(max_length=200,null=True,verbose_name=_('version'))
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False,
                                        verbose_name=_('production_form'))
    
    class Meta:
        db_table = 'production_software_requirements'
        verbose_name = _('ProductionSoftwareRequirement')
        verbose_name_plural = _('ProductionSoftwareRequirements')

    def __unicode__(self):
        return "%s" % (self.name)

    
class Milestone(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    description = models.CharField(max_length=200,null=False,verbose_name=_('description'))
    duration = models.CharField(max_length=50,null=True,verbose_name=_('duration'))
    created_at = models.DateTimeField(auto_now_add=True,verbose_name=_('created_at'))
    date_event = models.DateTimeField(null=True, blank=True, verbose_name=_('date_event'))
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False,
                                        verbose_name=_('production_form'))
    
    class Meta:
        db_table = 'milestones'
        verbose_name = _('Milestone')
        verbose_name_plural = _('Milestones')

    def __unicode__(self):
        return "%s" % (self.description)



class SCVPermission(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    user = models.CharField(max_length=200,null=False,verbose_name=_('user'))
    permission = models.CharField(max_length=50,null=False,verbose_name=_('permission'))
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False,
                                         verbose_name=_('application_form'))

    class Meta:
        db_table = 'scv_permissions'
        verbose_name = _('SCVPermission')
        verbose_name_plural = _('SCVPermissions')

    def __unicode__(self):
        return "%s %s" % (self.user, self.permission)

    @classmethod
    def permissions(cls):
        return (
            ('R', 'Read'),
            ('W', 'Write'),
            ('R/W', 'Read/Write'),
        )
    
class Referrer(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name   = models.CharField(max_length=200,null=False,verbose_name=_('name'))
    email  = models.CharField(max_length=200,null=True, validators=[validate_email],
                              verbose_name=_('email'))
    phones = models.CharField(max_length=200,null=True,verbose_name=_('phones'))
    is_applicant = models.BooleanField(default=False,null=False,verbose_name=_('is_applicant'))
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False,
                                         verbose_name=_('application_form'))

    class Meta:
        db_table = 'referrers'
        verbose_name = _('Referrer')
        verbose_name_plural = _('Referrers')


    def __unicode__(self):
        return "%s" % self.name


class MonitoredVariable(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name   = models.CharField(max_length=200,null=False,verbose_name=_('name'))
    periodicity  = models.CharField(max_length=200,null=True,verbose_name=_('periodicity'))
    preserving_history_by = models.CharField(max_length=200,null=True,verbose_name=_('preserving_history_by'))
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False,
                                        verbose_name=_('production_form'))

    class Meta:
        db_table = 'monitored_variables'
        verbose_name = _('MonitoredVariable')
        verbose_name_plural = _('MonitoredVariables')

    def __unicode__(self):
        return "%s" % self.name


class TestServer(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    virtual_machine_name = models.CharField(max_length=200,null=False,
                                            verbose_name=_('virtual_machine_name'))
    ip_address  = models.CharField(max_length=200,null=True,verbose_name=_('ip_address'))
    mac_address = models.CharField(max_length=200,null=True,verbose_name=_('mac_address'))
    ram_memory  = models.CharField(max_length=200,null=True,verbose_name=_('ram_memory'))
    disk_space  = models.CharField(max_length=200,null=True,verbose_name=_('disk_space'))
    processors = models.CharField(max_length=200,null=True,verbose_name=_('processors'))
    database_permissions = models.CharField(max_length=200,null=True,
                                            verbose_name=_('database_permissions'))
    database_server = models.CharField(max_length=200,null=True,verbose_name=_('database_server'))
    location_logs = models.CharField(max_length=200,null=True,verbose_name=_('location_logs'))
    cluster_virtual_machine = models.CharField(max_length=200,null=True,
                                               verbose_name=_('cluster_virtual_machine'))
    vcs_repository = models.CharField(max_length=200,null=True,verbose_name=_('vcs_repository'))
    observations = models.TextField(null=True, blank=True,verbose_name=_('observations'))
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False,
                                         verbose_name=_('application_form'))
    applicant = models.CharField(max_length=200, null=True, blank=True,verbose_name=_('applicant'))
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=_('user'))
    signature_date = models.DateTimeField(null=True, blank=True,auto_now_add=True,
                                          verbose_name=_('signature_date'))
    related_ticket = models.CharField(max_length=200,null=True,blank=True,verbose_name=_('related_ticket'))
    
    class Meta:
        db_table = 'test_servers'
        verbose_name = _('TestServer')
        verbose_name_plural = _('TestServers')

    def __unicode__(self):
        return "%s" % self.virtual_machine_name


class ProductionServer(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    virtual_machine_name = models.CharField(max_length=200,null=False,verbose_name=_('virtual_machine_name'))
    ip_address  = models.CharField(max_length=200,null=True,verbose_name=_('ip_address'))
    mac_address = models.CharField(max_length=200,null=True,verbose_name=_('mac_address'))
    ram_memory  = models.CharField(max_length=200,null=True,verbose_name=_('ram_memory'))
    disk_space  = models.CharField(max_length=200,null=True,verbose_name=_('disk_space'))
    processors = models.CharField(max_length=200,null=True,verbose_name=_('processors'))
    database_permissions = models.CharField(max_length=200,null=True,verbose_name=_('database_permissions'))
    database_server = models.CharField(max_length=200,null=True,verbose_name=_('database_server'))
    location_logs = models.CharField(max_length=200,null=True,verbose_name=_('location_logs'))
    cluster_virtual_machine = models.CharField(max_length=200,null=True,
                                               verbose_name=_('cluster_virtual_machine'))
    observations = models.TextField(null=True, blank=True,verbose_name=_('observations'))
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False,
                                        verbose_name=_('production_form'))    
    added_monitoring = models.BooleanField(default=False,null=False,verbose_name=_('added_monitoring'))
    added_backup     = models.BooleanField(default=False,null=False,verbose_name=_('added_backup'))

    applicant = models.CharField(max_length=200, null=True, blank=True,verbose_name=_('applicant'))
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=_('user'))
    signature_date = models.DateTimeField(null=True, blank=True,auto_now_add=True,
                                          verbose_name=_('signature_date'))
    related_ticket = models.CharField(max_length=200,null=True,blank=True,verbose_name=_('related_ticket'))
    
    class Meta:
        db_table = 'production_servers'
        verbose_name = _('ProductionServer')
        verbose_name_plural = _('ProductionServers')

    def __unicode__(self):
        return "%s" % self.virtual_machine_name
