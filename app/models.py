# -*- encoding: utf-8 -*-
from django.db import models
from datetime import datetime


class ConnectionSource(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    ip = models.CharField(max_length=200,null=True)
    observations = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'connection_sources'
        verbose_name_plural = 'ConnectionSources'

    def __unicode__(self):
        return "%s" % (self.name)

    
class ConnectionTarget(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    ip = models.CharField(max_length=200,null=True)
    ip_firewall  = models.CharField(max_length=200,null=True)
    observations = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'connection_targets'
        verbose_name_plural = 'ConnectionTargets'

    def __unicode__(self):
        return "%s" % (self.name)

    
class SoftwareRequirement(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    version = models.CharField(max_length=200,null=True)
    
    class Meta:
        db_table = 'software_requirements'
        verbose_name_plural = 'SoftwareRequirements'

    def __unicode__(self):
        return "%s" % (self.name)

    
class Proyect(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'proyects'
        verbose_name_plural = 'Proyects'

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

    connection_sources = models.ManyToManyField(ConnectionSource, blank=True)
    connection_targets = models.ManyToManyField(ConnectionTarget, blank=True)

    software_requirements = models.ManyToManyField(SoftwareRequirement, blank=True)
    
    class Meta:
        db_table = 'application_forms'
        verbose_name_plural = 'ApplicationForms'

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

    connection_sources = models.ManyToManyField(ConnectionSource, blank=True)
    connection_targets = models.ManyToManyField(ConnectionTarget, blank=True)

    software_requirements = models.ManyToManyField(SoftwareRequirement, blank=True)
        
    class Meta:
        db_table = 'production_forms'
        verbose_name_plural = 'ProductionForms'

    def __unicode__(self):
        return "%s" % (self.proyect.name)


class Milestone(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    description = models.CharField(max_length=200,null=False)
    duration = models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False)
    
    class Meta:
        db_table = 'milestones'
        verbose_name_plural = 'Milestones'

    def __unicode__(self):
        return "%s" % (self.description)



class SCVPermision(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    user = models.CharField(max_length=200,null=False)
    permision = models.CharField(max_length=50,null=False)
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False)    

    class Meta:
        db_table = 'scv_permisions'
        verbose_name_plural = 'SCVPermisions'

    def __unicode__(self):
        return "%s %s" % (self.user, self.permision)

    @classmethod
    def permisions(cls):
        return (
            ('R', 'Read'),
            ('W', 'Write'),
            ('R/W', 'Read/Write'),
        )
    
class Referrer(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name   = models.CharField(max_length=200,null=False)
    email  = models.CharField(max_length=200,null=True)
    phones = models.CharField(max_length=200,null=True)
    is_applicant = models.BooleanField(default=False,null=False)
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False)    

    class Meta:
        db_table = 'referrers'
        verbose_name_plural = 'Referrers'

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
        verbose_name_plural = 'MonitoredVariables'

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
        verbose_name_plural = 'TestServers'

    def __unicode__(self):
        return "%s" % self.virtual_machine_name

