# -*- encoding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.utils.translation import ugettext as _
from django.core.validators import validate_ipv46_address, validate_email
from django.contrib.auth.models import User
import datetime
from redmine import Redmine
from django.conf import settings
from helpers import to_v, to_absolute_url
import logging
from django.core.urlresolvers import reverse
import django.utils.timezone 
from pyzabbix import ZabbixAPI


class Zbbx():

    @classmethod
    def new(cls):
        try:
            zapi = ZabbixAPI( url=settings.ZABBIX_API_URL,
                              user=settings.ZABBIX_API_USERNAME,
                              password=settings.ZABBIX_API_PASSWORD)
            return zapi
        except Exception as e:
            logging.error("Could not connect to API Zabbix: '%s'" % settings.ZABBIX_API_URL )
            logging.error(e)
            return None

    @classmethod
    def get_template_ids(cls, hostname):
        tpls = []
        cnn = cls.new()

        if cnn is None:
            return tpls
        
        result = cnn.host.get( selectParentTemplates=1,
                                     filter={'host': hostname} )
        if len(result) > 0  and 'parentTemplates' in result[0]:
            for tpl in result[0]['parentTemplates']:
                tpls.append(tpl['templateid'])

        return tpls


    
class Proyect(models.Model):
    id = models.AutoField( primary_key=True,null=False)
    name = models.CharField( max_length=200,null=False,
                             verbose_name=_('name'))
    description = models.TextField( null=True, blank=True,
                                    verbose_name=_('description'))
    created_at = models.DateTimeField( auto_now_add=True,
                                       verbose_name=_('created_at'))
    updated_at = models.DateTimeField( auto_now=True,
                                       verbose_name=_('updated_at'))
    
    class Meta:
        db_table = 'proyects'
        verbose_name = _('Proyect')
        verbose_name_plural = _('Proyects')

    def __unicode__(self):
        return "%s" % (self.name)

    @classmethod
    def production_pass_enabled(cls):
        return Proyect.objects \
                      .filter(applicationform__testserver__application_form__isnull=False) \
                      .filter(productionform__productionserver__production_form__isnull=True) \
                      .order_by('name')

    
class ApplicationForm (models.Model):
    proyect = models.OneToOneField(Proyect, primary_key=True,
                                   verbose_name=_('proyect'))

    db_name = models.CharField(max_length=200, null=True, blank=True,
                               verbose_name=_('db_name'))
    encoding = models.CharField(max_length=200, null=True, blank=True,
                                verbose_name=_('encoding'))
    user_owner = models.CharField(max_length=200, null=True, blank=True,
                                  verbose_name=_('user_owner'))
    user_access = models.CharField(max_length=200, null=True, blank=True,
                                   verbose_name=_('user_access'))

    observations = models.TextField( null=True, blank=True,
                                     verbose_name=_('observations'))

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('updated_at'))
    signature_date = models.DateTimeField(null=True, blank=True,
                                          verbose_name=_('signature_date'))
    received_application = models.BooleanField(default=False,
                                               verbose_name=_('received_application'))
    
    class Meta:
        db_table = 'application_forms'
        verbose_name = _('ApplicationForm')
        verbose_name_plural = _('ApplicationForms')

    def __unicode__(self):
        return "%s" % (self.proyect.name)

    
class ProductionForm (models.Model):
    proyect = models.OneToOneField(Proyect, primary_key=True,
                                   verbose_name=_('proyect'))

    db_name = models.CharField(max_length=200, null=True, blank=True,
                               verbose_name=_('db_name'))
    encoding = models.CharField(max_length=200, null=True, blank=True,
                                verbose_name=_('encoding'))
    user_owner = models.CharField(max_length=200, null=True, blank=True,
                                  verbose_name=_('user_owner'))
    user_access = models.CharField(max_length=200, null=True, blank=True,
                                   verbose_name=_('user_access'))

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
    received_application = models.BooleanField(default=False,
                                               verbose_name=_('received_application'))
    
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
    ip = models.CharField(max_length=200, null=True,blank=True,
                          verbose_name=_('ip'),
                          validators=[validate_ipv46_address])
    service = models.CharField(max_length=200,null=True,blank=True,
                               verbose_name=_('service'))
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
    name = models.CharField(max_length=200,null=False,
                            verbose_name=_('name'))
    ip = models.CharField(max_length=200,null=True,blank=True,
                          verbose_name=_('ip'))
    service = models.CharField(max_length=200,null=True,blank=True,
                               verbose_name=_('service'))
    observations = models.TextField(null=True, blank=True,
                                    verbose_name=_('observations'))
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
    name = models.CharField(max_length=200,null=False,
                            verbose_name=_('name'))
    ip = models.CharField(max_length=200,null=True,blank=True,
                          verbose_name=_('ip'),
                          validators=[validate_ipv46_address])
    service = models.CharField(max_length=200,null=True,blank=True,
                               verbose_name=_('service'))
    observations = models.TextField(null=True, blank=True,
                                    verbose_name=_('observations'))
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
    name = models.CharField(max_length=200,null=False,
                            verbose_name=_('name'))
    ip = models.CharField(max_length=200,null=True,blank=True,
                          verbose_name=_('ip'))
    ip_firewall  = models.CharField(max_length=200,null=True,blank=True,
                                    verbose_name=_('ip_firewall'))
    service = models.CharField(max_length=200,null=True,blank=True,
                               verbose_name=_('service'))
    port = models.CharField(max_length=200, null=True, blank=True,
                            verbose_name=_('port'))
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
    name = models.CharField(max_length=200,null=False,
                            verbose_name=_('name'))
    version = models.CharField(max_length=200,null=True,
                               verbose_name=_('version'))
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False,
                                         verbose_name=_('application_form'))
    
    class Meta:
        db_table = 'application_software_requirements'
        verbose_name = _('ApplicationSoftwareRequirement')
        verbose_name_plural = _('ApplicationSoftwareRequirements')

    def __unicode__(self):
        return "%s" % (self.name)

    @classmethod
    def by_proyect(cls,proyect_id):
        return ApplicationSoftwareRequirement.objects \
                                             .select_related('application_form__proyect') \
                                             .filter(application_form__proyect=proyect_id)


    
    
class ProductionSoftwareRequirement(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name = models.CharField(max_length=200,null=False,
                            verbose_name=_('name'))
    version = models.CharField(max_length=200,null=True,
                               verbose_name=_('version'))
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
    description = models.CharField(max_length=200,null=False,
                                   verbose_name=_('description'))
    duration = models.CharField(max_length=50,null=True,
                                verbose_name=_('duration'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('created_at'))
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
    user = models.CharField(max_length=200,null=False,
                            verbose_name=_('user'))
    permission = models.CharField(max_length=50,null=False,
                                  verbose_name=_('permission'))
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
    name   = models.CharField(max_length=200,null=False,
                              verbose_name=_('name'))
    email  = models.CharField(max_length=200,null=True, blank=True,
                              validators=[validate_email],
                              verbose_name=_('email'))
    phones = models.CharField(max_length=200,null=True, blank=True,
                              verbose_name=_('phones'))
    is_applicant = models.BooleanField(default=False,null=False,
                                       verbose_name=_('is_applicant'))
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False,
                                         verbose_name=_('application_form'))

    class Meta:
        db_table = 'referrers'
        verbose_name = _('Referrer')
        verbose_name_plural = _('Referrers')


    def __unicode__(self):
        return "%s" % self.name

    @classmethod
    def to_emails_by_application_form(cls, application_form_id):
        referrers = Referrer.objects.filter(application_form=application_form_id)
        emails = []
        for item in referrers:
            emails.append(item.email)
        return emails

class MonitoredVariable(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    name   = models.CharField(max_length=200,null=False,
                              verbose_name=_('name'))
    periodicity  = models.CharField(max_length=200,null=True,
                                    verbose_name=_('periodicity'))
    preserving_history_by = models.CharField(max_length=200,null=True,
                                             verbose_name=_('preserving_history_by'))
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
    ip_address  = models.CharField(max_length=200,null=True,blank=True,
                                   verbose_name=_('ip_address'))
    mac_address = models.CharField(max_length=200,null=True,
                                   verbose_name=_('mac_address'))
    ram_memory  = models.CharField(max_length=200,null=True,
                                   verbose_name=_('ram_memory'))
    disk_space  = models.CharField(max_length=200,null=True,
                                   verbose_name=_('disk_space'))
    processors = models.CharField(max_length=200,null=True,
                                  verbose_name=_('processors'))
    database_permissions = models.TextField(null=True,blank=True,
                                            verbose_name=_('database_permissions'))
    database_server = models.CharField(max_length=200,null=True,
                                       verbose_name=_('database_server'))
    location_logs = models.TextField(null=True,blank=True,
                                     verbose_name=_('location_logs'))
    cluster_virtual_machine = models.CharField(max_length=200,null=True,
                                               verbose_name=_('cluster_virtual_machine'))
    vcs_repository = models.CharField(max_length=200,null=True,blank=True,
                                      verbose_name=_('vcs_repository'))
    observations = models.TextField(null=True, blank=True,
                                    verbose_name=_('observations'))
    application_form = models.ForeignKey(ApplicationForm, null=False, blank=False,
                                         verbose_name=_('application_form'))
    applicant = models.CharField(max_length=200, null=True, blank=True,
                                 verbose_name=_('applicant'))
    user = models.ForeignKey(User, null=True, blank=True,
                             verbose_name=_('user'))
    signature_date = models.DateTimeField(default=django.utils.timezone.now, null=False,
                                          verbose_name=_('signature_date'))
    related_ticket = models.CharField(max_length=200,null=True,blank=True,
                                      verbose_name=_('related_ticket'))
    url = models.CharField(max_length=200,null=True,blank=True,
                           verbose_name=_('url'))
    
    class Meta:
        db_table = 'test_servers'
        verbose_name = _('TestServer')
        verbose_name_plural = _('TestServers')

    def __unicode__(self):
        return "%s" % self.virtual_machine_name


class ProductionServer(models.Model):
    id = models.AutoField(primary_key=True,null=False)
    virtual_machine_name = models.CharField(max_length=200,null=False,
                                            verbose_name=_('virtual_machine_name'))
    ip_address  = models.CharField(max_length=200,null=True,
                                   verbose_name=_('ip_address'))
    mac_address = models.CharField(max_length=200,null=True,
                                   verbose_name=_('mac_address'))
    ram_memory  = models.CharField(max_length=200,null=True,
                                   verbose_name=_('ram_memory'))
    disk_space  = models.CharField(max_length=200,null=True,
                                   verbose_name=_('disk_space'))
    processors = models.CharField(max_length=200,null=True,
                                  verbose_name=_('processors'))
    database_permissions = models.TextField(null=True,blank=True,
                                            verbose_name=_('database_permissions'))
    database_server = models.CharField(max_length=200,null=True,
                                       verbose_name=_('database_server'))
    location_logs = models.TextField(null=True,blank=True,
                                     verbose_name=_('location_logs'))
    cluster_virtual_machine = models.CharField(max_length=200,null=True,
                                               verbose_name=_('cluster_virtual_machine'))
    observations = models.TextField(null=True, blank=True,
                                    verbose_name=_('observations'))
    production_form = models.ForeignKey(ProductionForm, null=False, blank=False,
                                        verbose_name=_('production_form'))
    # FIME: will be removed
    added_monitoring = models.BooleanField(default=False,null=False,
                                           verbose_name=_('added_monitoring'))
    # FIME: will be removed
    added_backup     = models.BooleanField(default=False,null=False,
                                           verbose_name=_('added_backup'))

    applicant = models.CharField(max_length=200, null=True, blank=True,
                                 verbose_name=_('applicant'))
    user = models.ForeignKey(User, null=True, blank=True,
                             verbose_name=_('user'))
    signature_date = models.DateTimeField(default=django.utils.timezone.now, null=False,
                                          verbose_name=_('signature_date'))
    related_ticket = models.CharField(max_length=200,null=True,blank=True,
                                      verbose_name=_('related_ticket'))
    url = models.CharField(max_length=200,null=True,blank=True,
                           verbose_name=_('url'))
    
    class Meta:
        db_table = 'production_servers'
        verbose_name = _('ProductionServer')
        verbose_name_plural = _('ProductionServers')

        
    # def zabbix_added_monitoring(self):
    #     Zbbx.is_monitored_host()
        
    # zabbix_added_monitoring.boolean = True
    # zabbix_added_monitoring.short_description = _("zabbix_added_monitoring")
        

    def __unicode__(self):
        return "%s" % self.virtual_machine_name


class TicketSystem(models.Model):

    @classmethod
    def connect(cls):
        try:
            return Redmine(settings.REDMINE_URL,
                           username=settings.REDMINE_USERNAME,
                           password=settings.REDMINE_PASSWORD)
        except Exception as e:
            logging.error("could not connect to %s" % settings.REDMINE_URL)
            logging.error(e)

    @classmethod
    def watchers_ids_by(cls,patterns):
        watchers = []
        for pattern in patterns:
            users_found = TicketSystem.find_user(pattern)
            for k,user in enumerate(users_found):
                watchers.append(user['id'])
        return watchers
            
    @classmethod
    def create_issue(cls,subject,description, watchers=[]):
        try:
            params = { 'project_id': settings.REDMINE_PROJECT,
                       'tracker_id': settings.REDMINE_TRACKER_ID,
                       'status_id': settings.REDMINE_STATUS_ID,
                       'priority_id': settings.REDMINE_PRIORITY_ID,
                       'assigned_to_id': settings.REDMINE_ASSIGNED_TO_ID,
                       'subject': subject,
                       'watcher_user_ids': watchers,
                       'description': description,
            }
            redmine = TicketSystem.connect()
            issue = redmine.issue.create( **params )
            return issue
        except Exception as e:
            logging.error(e)
            
    @classmethod
    def find_user(cls,name_to_search):
        users_found = []
        try:
            redmine = TicketSystem.connect()
            users = redmine.user.filter(name=name_to_search)
            if len(users) < settings.REDMINE_MAXIMUM_OBSERVER_FOUND:
                for user in users:
                    users_found.append({'id':user.id,
                                        'mail':user.mail,
                                        'firstname':user.firstname,
                                        'lastname': user.lastname})
            return users_found
        except Exception as e:
            logging.error(e)
            return users_found


        
    @classmethod
    def format_application_description_issue(cls,app):
        software = ApplicationSoftwareRequirement.objects.filter(application_form=app.pk)
        sources = ApplicationConnectionSource.objects.filter(application_form=app.pk)
        targets = ApplicationConnectionTarget.objects.filter(application_form=app.pk)
        csv_permission = SCVPermission.objects.filter(application_form=app.pk)
        referrers = Referrer.objects.filter(application_form=app.pk)
        
        description =  "* *%s*: %s\n" % (_('proyect_name'), app.proyect.name)

        if app.observations:
            description += "* %s: <pre>%s</pre>\n" % (_('observations'), app.observations)

        if app.db_name or app.encoding or app.user_owner or app.user_access:
            description += "\n* %s\n" % _('database')
            description += "<pre>"
            description += "%s: %s\n" % (_('name'), app.db_name)
            description += "%s: %s\n" % (_('encoding'), app.encoding)
            description += "%s: %s\n" % (_('user_owner'), app.user_owner)
            description += "%s: %s\n" % (_('user_access'), app.user_access)
            description += "</pre>"
            
        if software:
            description += "\n* %s [%s, %s]\n" % ( _('software_requirements'),
                                                   _('name'),
                                                   _('version'))
            description += "<pre>"
            for item in software:
                description += "%s %s\n" % (item.name, to_v(item.version))
            description += "</pre>"

        if sources:
            description += "\n* %s [%s, %s, %s, %s]\n" % ( _('connection_sources'),
                                                           _('name'),
                                                           _('ip_address'),
                                                           _('service'),
                                                           _('observations'))
            description += "<pre>"
            for item in sources:
                description += "%s, %s, %s, %s\n" % (item.name,
                                                     to_v(item.ip),
                                                     to_v(item.service),
                                                     to_v(item.observations))
            description += "</pre>"
                
        if targets:
            description += "\n* %s [%s, %s, %s, %s]\n" % ( _('connection_targets'),
                                                           _('name'),
                                                           _('ip_address'),
                                                           _('service'),
                                                           _('observations'))
            description += "<pre>"
            for item in targets:
                description += "%s, %s, %s, %s\n" % (item.name,
                                                     to_v(item.ip),
                                                     to_v(item.service),
                                                     to_v(item.observations))
            description += "</pre>"

        if csv_permission:
            description += "\n* %s [%s, %s]\n" % ( _('vcs_repository'),
                                                   _('users'),
                                                   _('permissions'), )
            description += "<pre>"
            for item in csv_permission:
                description += "%s, %s\n" % (item.user,
                                             item.permission)
            description += "</pre>"

        if referrers:
            description += "\n* %s [%s, %s, %s, %s]\n" % ( _('applicants_and_referentes'),
                                                           _('name_and_surname'),
                                                           _('email'),
                                                           _('phones'),
                                                           _('is_applicant'))
            description += "<pre>"
            for item in referrers:
                is_applicant = ""
                if item.is_applicant:
                    is_applicant = _('yes')
                description += "%s, %s, %s, %s\n" % (item.name,
                                                     to_v(item.email),
                                                     to_v(item.phones),
                                                     is_applicant)
            description += "</pre>"

            description += "\n* %s" % (_('remember_to_add_server') \
                                     % {'url': to_absolute_url(reverse ('admin:app_testserver_add')),
                                        'name': _('title')})

        return description

    @classmethod
    def format_production_description_issue(cls,app):
        software = ProductionSoftwareRequirement.objects.filter(production_form=app.pk)
        sources = ProductionConnectionSource.objects.filter(production_form=app.pk)
        targets = ProductionConnectionTarget.objects.filter(production_form=app.pk)
        variables = MonitoredVariable.objects.filter(production_form=app.pk)
        hitos = Milestone.objects.filter(production_form=app.pk)
    
        description =  "* *%s*: %s\n" % (_('proyect_name'), app.proyect.name)

        if app.applicant:
            description +=  "* %s: %s\n" % (_('applicant'), app.applicant)

        if app.observations:
            description += "* %s: <pre>%s</pre>\n" % (_('observations'), app.observations)

        if app.db_name or app.encoding or app.user_owner or app.user_access:
            description += "\n* %s\n" % _('database')
            description += "<pre>"
            description += "%s: %s\n" % (_('name'), app.db_name)
            description += "%s: %s\n" % (_('encoding'), app.encoding)
            description += "%s: %s\n" % (_('user_owner'), app.user_owner)
            description += "%s: %s\n" % (_('user_access'), app.user_access)
            description += "</pre>"

        if app.db_space_to_start or app.db_space_at_year or app.db_space_after:
            description += "\n* %s - %s\n" % (_('estimated_volume_data'), _('database') )
            description += "<pre>"
            description += "%s: %s\n" % (_('space_to_start'), app.db_space_to_start)
            description += "%s: %s\n" % (_('space_at_year'), app.db_space_at_year)
            description += "%s: %s\n" % (_('space_after'), app.db_space_after)
            description += "</pre>"
        if app.fs_space_to_start or app.fs_space_at_year or app.fs_space_after:
            description += "\n* %s - %s\n" % (_('estimated_volume_data'), _('filesystem') )
            description += "<pre>"
            description += "%s: %s\n" % (_('space_to_start'), app.fs_space_to_start)
            description += "%s: %s\n" % (_('space_at_year'), app.fs_space_at_year)
            description += "%s: %s\n" % (_('space_after'), app.fs_space_after)
            description += "</pre>"

        if app.minimum_memory or app.suggested_memory or \
           app.minimum_disk_space or app.suggested_disk_space or \
           app.minimum_processor or app.suggested_processor:
            description += "\n* %s\n" % _('hardware_requirements')
            description += "<pre>"
            description += "%s: \t %s: %s \t %s: %s\n" % ( _('memory'),
                                                           _('minimum'), app.minimum_memory,
                                                           _('recommended'), app.suggested_memory )
            description += "%s: \t %s: %s \t %s: %s\n" % ( _('disk'),
                                                           _('minimum'),app.minimum_disk_space,
                                                           _('recommended'),app.suggested_disk_space )
            description += "%s: \t %s: %s \t %s: %s\n" % ( _('processor'),
                                                           _('minimum'),app.minimum_processor,
                                                           _('recommended'), app.suggested_processor )
            description += "</pre>"

        if software:
            description += "\n* %s [%s, %s]\n" % ( _('software_requirements'),
                                                   _('name'),
                                                   _('version'))
            description += "<pre>"
            for item in software:
                description += "%s, %s\n" % (item.name, to_v(item.version))
            description += "</pre>"

        if sources:
            description += "\n* %s [%s, %s, %s, %s]\n" % ( _('connection_sources'),
                                                           _('name'),
                                                           _('ip_address'),
                                                           _('service'),
                                                           _('observations'))
            description += "<pre>"
            for item in sources:
                description += "%s, %s, %s, %s\n" % (item.name,
                                                     to_v(item.ip),
                                                     to_v(item.service),
                                                     to_v(item.observations))
            description += "</pre>"
                
        if targets:
            description += "\n* %s [%s, %s, %s, %s, %s]\n" % ( _('connection_targets'),
                                                           _('name'),
                                                           _('ip_address'),
                                                           _('service'),
                                                           _('port'),
                                                           _('ip_firewall'))
            description += "<pre>"
            for item in targets:
                description += "%s, %s, %s, %s, %s\n" % (item.name,
                                                     to_v(item.ip),
                                                     to_v(item.service),
                                                     to_v(item.port),
                                                     to_v(item.ip_firewall))
            description += "</pre>"


        if variables:
            description += "\n* %s [%s, %s, %s]\n" % ( _('variables_to_be_monitored'),
                                                       _('variable'),
                                                       _('periodicity'),
                                                       _('preserving_history_by') )
            description += "<pre>"
            for item in variables:
                description += "%s, %s, %s\n" % (item.name,
                                            to_v(item.periodicity),
                                            to_v(item.preserving_history_by))
            description += "</pre>"

        if hitos:
            description += "\n* %s [%s, %s, %s]\n" % ( _('milestones_during_the_year'),
                                                   _('milestone'),
                                                   _('date'),
                                                   _('duration_in_days') )
            description += "<pre>"
            for item in hitos:
                description += "%s, %s, %s\n" % (item.description,
                                                 to_v(str(item.date_event.strftime("%d/%m/%Y %H:%M"))),
                                                 to_v(item.duration))
            description += "</pre>"

        if app.files_backup:
            description += "\n* %s: <pre>%s</pre>\n" % (_('files_backup'), app.files_backup)


        description += "\n* %s" % (_('remember_to_add_server') \
                                % {'url': to_absolute_url(reverse ('admin:app_productionserver_add')),
                                'name': _('title')})

    
        return description
