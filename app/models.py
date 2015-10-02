# -*- encoding: utf-8 -*-
from django.db import models
from datetime import datetime


class ConnectionSource(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    ip = models.CharField(max_length=200,null=True)
    observations = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = 'connection_source'
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
        db_table = 'connection_target'
        verbose_name_plural = 'ConnectionTargets'

    def __unicode__(self):
        return "%s" % (self.name)

class SoftwareRequirement(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False)
    version = models.CharField(max_length=200,null=True)
    
    class Meta:
        db_table = 'software_requirement'
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
        db_table = 'application_form'
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
        db_table = 'production_form'
        verbose_name_plural = 'ProductionForms'

    def __unicode__(self):
        return "%s" % (self.proyect.name)


