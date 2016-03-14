# -*- encoding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils.translation import ugettext as _
from django.core.validators import validate_ipv46_address, validate_email

    
class Proyect(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'proyects'
        verbose_name = _('Proyect')
        verbose_name_plural = _('Proyects')

    def __unicode__(self):
        return "%s" % (self.name)

    
class ApplicationForm (models.Model):
    proyect = models.OneToOneField(Proyect, primary_key=True)

    db_name = models.CharField(max_length=200, null=True, blank=True)
    encoding = models.CharField(max_length=200, null=True, blank=True)
    user_owner = models.CharField(max_length=200, null=True, blank=True)
    user_access = models.CharField(max_length=200, null=True, blank=True)

    observations = models.TextField( null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    signature_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'application_forms'
        verbose_name = _('ApplicationForm')
        verbose_name_plural = _('ApplicationForms')

    def __unicode__(self):
        return "%s" % (self.proyect.name)

    
class ProductionForm (models.Model):
    proyect = models.OneToOneField(Proyect, primary_key=True)

    db_name = models.CharField(max_length=200, null=True, blank=True)
    encoding = models.CharField(max_length=200, null=True, blank=True)
    user_owner = models.CharField(max_length=200, null=True, blank=True)
    user_access = models.CharField(max_length=200, null=True, blank=True)

    db_space_to_start = models.CharField(max_length=200, null=True, blank=True)
    db_space_at_year  = models.CharField(max_length=200, null=True, blank=True)
    db_space_after    = models.CharField(max_length=200, null=True, blank=True)

    fs_space_to_start = models.CharField(max_length=200, null=True, blank=True)
    fs_space_at_year  = models.CharField(max_length=200, null=True, blank=True)
    fs_space_after    = models.CharField(max_length=200, null=True, blank=True)

    minimum_memory = models.CharField(max_length=200, null=True, blank=True)
    minimum_disk_space = models.CharField(max_length=200, null=True, blank=True)
    minimum_processor = models.CharField(max_length=200, null=True, blank=True)

    suggested_memory = models.CharField(max_length=200, null=True, blank=True)
    suggested_disk_space = models.CharField(max_length=200, null=True, blank=True)
    suggested_processor = models.CharField(max_length=200, null=True, blank=True)

    files_backup = models.TextField( null=True, blank=True)
    observations = models.TextField( null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    applicant = models.CharField(max_length=200, null=True, blank=True)
    signature_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'production_forms'
        verbose_name = _('ProductionForm')
        verbose_name_plural = _('ProductionForms')

    def __unicode__(self):
        return "%s" % (self.proyect.name)


class ApplicationConnectionSource(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    ip = models.CharField(max_length=200, null=True, validators=[validate_ipv46_address])
    observations = models.TextField(null=True, blank=True)
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False)
    
    class Meta:
        db_table = 'application_connection_sources'
        verbose_name = _('ApplicationConnectionSource')
        verbose_name_plural = _('ApplicationConnectionSources')

    def __unicode__(self):
        return "%s" % (self.name)

    
class ProductionConnectionSource(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    ip = models.CharField(max_length=200,null=True)
    observations = models.TextField(null=True, blank=True)
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False)
    
    class Meta:
        db_table = 'production_connection_sources'
        verbose_name = _('ProductionConnectionSource')
        verbose_name_plural = _('ProductionConnectionSources')

    def __unicode__(self):
        return "%s" % (self.name)

    
class ApplicationConnectionTarget(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    ip = models.CharField(max_length=200,null=True, validators=[validate_ipv46_address])
    observations = models.TextField(null=True, blank=True)
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False)
    
    class Meta:
        db_table = 'application_connection_targets'
        verbose_name = _('ApplicationConnectionTarget')
        verbose_name_plural = _('ApplicationConnectionTargets')

    def __unicode__(self):
        return "%s" % (self.name)

class ProductionConnectionTarget(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    ip = models.CharField(max_length=200,null=True)
    ip_firewall  = models.CharField(max_length=200,null=True)
    observations = models.TextField(null=True, blank=True)
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False)
        
    class Meta:
        db_table = 'production_connection_targets'
        verbose_name = _('ProductionConnectionTarget')
        verbose_name_plural = _('ProductionConnectionTargets')

    def __unicode__(self):
        return "%s" % (self.name)

    
class ApplicationSoftwareRequirement(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    version = models.CharField(max_length=200,null=True)
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False)
    
    class Meta:
        db_table = 'application_software_requirements'
        verbose_name = _('ApplicationSoftwareRequirement')
        verbose_name_plural = _('ApplicationSoftwareRequirements')

    def __unicode__(self):
        return "%s" % (self.name)

    
class ProductionSoftwareRequirement(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    version = models.CharField(max_length=200,null=True)
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False)
    
    class Meta:
        db_table = 'production_software_requirements'
        verbose_name = _('ProductionSoftwareRequirement')
        verbose_name_plural = _('ProductionSoftwareRequirements')

    def __unicode__(self):
        return "%s" % (self.name)

class Milestone(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    description = models.CharField(max_length=200,null=False)
    duration = models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False)
    
    class Meta:
        db_table = 'milestones'
        verbose_name = _('Milestone')
        verbose_name_plural = _('Milestones')

    def __unicode__(self):
        return "%s" % (self.description)



class SCVPermission(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    user = models.CharField(max_length=200,null=False)
    permission = models.CharField(max_length=50,null=False)
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False)    

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
    name   = models.CharField(max_length=200,null=False)
    email  = models.CharField(max_length=200,null=True, validators=[validate_email])
    phones = models.CharField(max_length=200,null=True)
    is_applicant = models.BooleanField(default=False,null=False)
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False)    

    class Meta:
        db_table = 'referrers'
        verbose_name = _('Referrer')
        verbose_name_plural = _('Referrers')


    def __unicode__(self):
        return "%s" % self.name


class MonitoredVariable(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name   = models.CharField(max_length=200,null=False)
    periodicity  = models.CharField(max_length=200,null=True)
    preserving_history_by = models.CharField(max_length=200,null=True)
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False)    

    class Meta:
        db_table = 'monitored_variables'
        verbose_name = _('MonitoredVariable')
        verbose_name_plural = _('MonitoredVariables')

    def __unicode__(self):
        return "%s" % self.name


class TestServer(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    virtual_machine_name = models.CharField(max_length=200,null=False)
    ip_address  = models.CharField(max_length=200,null=True)
    mac_address = models.CharField(max_length=200,null=True)
    ram_memory  = models.CharField(max_length=200,null=True)
    disk_space  = models.CharField(max_length=200,null=True)
    processors = models.CharField(max_length=200,null=True)
    database_permissions = models.CharField(max_length=200,null=True)
    database_server = models.CharField(max_length=200,null=True)
    location_logs = models.CharField(max_length=200,null=True)
    cluster_virtual_machine = models.CharField(max_length=200,null=True)
    vcs_repository = models.CharField(max_length=200,null=True)
    observations = models.TextField(null=True, blank=True)
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False)    

    applicant = models.CharField(max_length=200, null=True, blank=True)
    signature_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'test_servers'
        verbose_name = _('TestServer')
        verbose_name_plural = _('TestServers')

    def __unicode__(self):
        return "%s" % self.virtual_machine_name


class ProductionServer(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    virtual_machine_name = models.CharField(max_length=200,null=False)
    ip_address  = models.CharField(max_length=200,null=True)
    mac_address = models.CharField(max_length=200,null=True)
    ram_memory  = models.CharField(max_length=200,null=True)
    disk_space  = models.CharField(max_length=200,null=True)
    processors = models.CharField(max_length=200,null=True)
    database_permissions = models.CharField(max_length=200,null=True)
    database_server = models.CharField(max_length=200,null=True)
    location_logs = models.CharField(max_length=200,null=True)
    cluster_virtual_machine = models.CharField(max_length=200,null=True)
    observations = models.TextField(null=True, blank=True)
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False)    
    added_monitoring = models.BooleanField(default=False,null=False)
    added_backup     = models.BooleanField(default=False,null=False)

    applicant = models.CharField(max_length=200, null=True, blank=True)
    signature_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'production_servers'
        verbose_name = _('ProductionServer')
        verbose_name_plural = _('ProductionServers')

    def __unicode__(self):
        return "%s" % self.virtual_machine_name
