from django.db import models
from datetime import datetime


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
    
    class Meta:
        db_table = 'application_form'
        verbose_name_plural = 'ApplicationForms'

    def __unicode__(self):
        return "%s" % (self.proyect.name)


