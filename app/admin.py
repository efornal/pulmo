# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from app.models import Proyect, ApplicationForm, ProductionForm, TicketSystem
from app.models import ApplicationConnectionTarget, ApplicationConnectionSource
from app.models import ProductionConnectionTarget, ProductionConnectionSource
from app.models import ApplicationSoftwareRequirement, ProductionSoftwareRequirement
from app.models import Milestone, SCVPermission, Referrer, MonitoredVariable
from app.models import TestServer, ProductionServer, User
from app.models import Zbbx
from django.forms import ModelForm
from django.forms.widgets import Textarea
from django.db import models
import logging

from django.utils.translation import ugettext as _
from django.contrib import messages
from django.conf import settings


class ApplicationFormForm(forms.ModelForm):
    logs_visualization = forms.ChoiceField(choices=settings.LOGS_VISUALIZATION_CHOICES)

    
class ProyectAdmin(admin.ModelAdmin):
    list_display = ('name', 'secretariat', 'updated_at', 'created_at')
    search_fields = ['name','secretariat','description']
    ordering = ('name',)
    list_filter = ('secretariat',)

    
class ReferrerInline(admin.TabularInline):
     model = Referrer
     fk_name = "application_form"
     extra = 0

     
class SCVPermissionInline(admin.TabularInline):
     model = SCVPermission
     fk_name = "application_form"
     extra = 0

     
class ApplicationConnectionSourceInline(admin.TabularInline):
     model = ApplicationConnectionSource
     fk_name = "application_form"
     extra = 0

     
class ApplicationConnectionTargetInline(admin.TabularInline):
     model = ApplicationConnectionTarget
     fk_name = "application_form"
     extra = 0

     
class ApplicationSoftwareRequirementInline(admin.TabularInline):
     model = ApplicationSoftwareRequirement
     fk_name = "application_form"
     extra = 0

          
class ApplicationFormAdmin(admin.ModelAdmin):
    model = ApplicationForm
    form = ApplicationFormForm
    list_display = ('proyect', 'requires_integration','received_application',
                    'related_ticket', 'signature_date')
    inlines = [
        ApplicationSoftwareRequirementInline,
        ApplicationConnectionSourceInline,
        ApplicationConnectionTargetInline,
        SCVPermissionInline,
        ReferrerInline,
    ]
    search_fields = ['proyect__name']
    list_filter = ('received_application','requires_integration')
    ordering = ('proyect__name',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 3,})},
    }
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('signature_date',)
        return self.readonly_fields

        
class ProductionConnectionSourceInline(admin.TabularInline):
     model = ProductionConnectionSource
     fk_name = "production_form"
     extra = 0

     
class ProductionConnectionTargetInline(admin.TabularInline):
     model = ProductionConnectionTarget
     fk_name = "production_form"
     extra = 0

     
class ProductionSoftwareRequirementInline(admin.TabularInline):
     model = ProductionSoftwareRequirement
     fk_name = "production_form"
     extra = 0

     
class MonitoredVariableInline(admin.TabularInline):
    model = MonitoredVariable
    fk_name = "production_form"
    extra = 0

    
class MilestoneInline(admin.TabularInline):
    model = Milestone
    fk_name = "production_form"
    extra = 0

    
class ProductionFormAdmin(admin.ModelAdmin):
    model = ProductionForm
    list_display = ('proyect','received_application', 'applicant',
                    'related_ticket','signature_date')
    inlines = [
        ProductionSoftwareRequirementInline,
        ProductionConnectionSourceInline,
        ProductionConnectionTargetInline,
        MonitoredVariableInline,
        MilestoneInline,
    ]
    search_fields = ['proyect__name']
    list_filter = ('received_application','applicant')
    ordering = ('proyect__name',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 3,})},
    }

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('signature_date',)
        return self.readonly_fields
    
    
class ApplicationFormAdminForm(forms.ModelForm):

    class Meta:
        model = ApplicationForm
        fields = '__all__'

    
class ApplicationConnectionSourceAdminForm(forms.ModelForm):

    class Meta:
        model = ApplicationConnectionSource
        fields = '__all__'

class ApplicationConnectionSourceAdmin(admin.ModelAdmin):
    form = ApplicationConnectionSourceAdminForm

    
class ApplicationConnectionTargetAdminForm(forms.ModelForm):

    class Meta:
        model = ApplicationConnectionTarget
        fields = '__all__'

class ApplicationConnectionTargetAdmin(admin.ModelAdmin):
    form = ApplicationConnectionTargetAdminForm
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 2,})},
    }

    
class SCVPermissionAdminForm(forms.ModelForm):
    permission = forms.ChoiceField(choices = SCVPermission.permissions())

    class Meta:
        model = SCVPermission
        fields = '__all__'
        
class SCVPermissionAdmin(admin.ModelAdmin):
    form = SCVPermissionAdminForm


class TestServerAdmin(admin.ModelAdmin):
    exclude = ('applicant',)
    ordering = ('application_form__proyect__name',)
    list_display = ('virtual_machine_name', 'ip_address',
                    'cluster_virtual_machine','related_ticket','user')
    search_fields = ['virtual_machine_name','ip_address']
    list_filter = ('cluster_virtual_machine',)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 3,})},
    }

    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user','signature_date')
        return self.readonly_fields
            

    def add_view(self, *args, **kwargs):
        self.exclude += ('user','signature_date')
        return super(TestServerAdmin, self).add_view(*args, **kwargs)


    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not obj.pk:
            obj.applicant = request.user.username # FIXME, temporal
            #obj.applicant = obj.user.username
            logging.info("The application server test has been signed by the user %s" \
                         % obj.applicant)
        
        super(TestServerAdmin, self).save_model(request, obj, form, change)


class ProductionServerAdmin(admin.ModelAdmin):
    #FIXME, backup and monitoring will be removed from db
    exclude = ('applicant','added_monitoring','added_backup')
    
    ordering = ('production_form__proyect__name',)
    list_display = ('virtual_machine_name', 'ip_address',
                    'cluster_virtual_machine','related_ticket','user')
    search_fields = ['virtual_machine_name','ip_address']
    list_filter = ('cluster_virtual_machine',)
    
    if hasattr(settings, 'ZABBIX_API_MONITORING_TEMPLATE_ID'):
        list_display += ('zabbix_added_monitoring',)
    if hasattr(settings, 'ZABBIX_API_PGSQL_TEMPLATE_ID'):
        list_display += ('zabbix_added_pgsql_backup',)
    if hasattr(settings, 'ZABBIX_API_MYSQL_TEMPLATE_ID'):
        list_display += ('zabbix_added_mysql_backup',)
        
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 3,})},
    }

    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user','signature_date')
        return self.readonly_fields

    
    def add_view(self, *args, **kwargs):
        self.exclude += ('user','signature_date')
        return super(ProductionServerAdmin, self).add_view(*args, **kwargs)

    
    def zabbix_added_mysql_backup(cls,obj):
        if hasattr(settings, 'ZABBIX_API_MYSQL_TEMPLATE_ID'):
            tpls = Zbbx.get_template_ids(obj.virtual_machine_name)
            return ("%s" % settings.ZABBIX_API_MYSQL_TEMPLATE_ID in tpls)
        return None
    zabbix_added_mysql_backup.short_description = _('added_mysql_backup')
    zabbix_added_mysql_backup.boolean = True

    
    def zabbix_added_pgsql_backup(cls,obj):
        if hasattr(settings, 'ZABBIX_API_PGSQL_TEMPLATE_ID'):
            tpls = Zbbx.get_template_ids(obj.virtual_machine_name)
            return ("%s" % settings.ZABBIX_API_PGSQL_TEMPLATE_ID in tpls)
        return None
    zabbix_added_pgsql_backup.short_description = _('added_pgsql_backup')
    zabbix_added_pgsql_backup.boolean = True

    
    def zabbix_added_monitoring(cls,obj):
        if hasattr(settings, 'ZABBIX_API_MONITORING_TEMPLATE_ID'):
            tpls = Zbbx.get_template_ids(obj.virtual_machine_name)
            return ("%s" % settings.ZABBIX_API_MONITORING_TEMPLATE_ID in tpls)
        return None
    zabbix_added_monitoring.short_description = _('added_monitoring')
    zabbix_added_monitoring.boolean = True

    
    def get_changeform_initial_data(self, request):
        return {'user': request.user.id }

    
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not obj.pk:
            obj.applicant = obj.user.username # FIXME, temporal
            #obj.applicant = request.user.username # FIXME, 
            logging.info("The application server production has been signed by the user %s" \
                         % obj.applicant)
            
        super(ProductionServerAdmin, self).save_model(request, obj, form, change)
        

    
admin.site.register(ApplicationForm,ApplicationFormAdmin)
admin.site.register(ProductionForm,ProductionFormAdmin)
admin.site.register(Proyect, ProyectAdmin)
admin.site.register(TestServer,TestServerAdmin)
admin.site.register(ProductionServer,ProductionServerAdmin)

