from django import forms
from django.contrib import admin
from app.models import Proyect, ApplicationForm, ProductionForm
from app.models import ApplicationConnectionTarget, ApplicationConnectionSource
from app.models import ProductionConnectionTarget, ProductionConnectionSource
from app.models import ApplicationSoftwareRequirement, ProductionSoftwareRequirement
from app.models import Milestone, SCVPermission, Referrer, MonitoredVariable
from app.models import TestServer, ProductionServer
from django.forms import ModelForm
from django.forms.widgets import Textarea
from django.db import models
import logging

class ProyectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ['name']

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
    inlines = [
        ApplicationSoftwareRequirementInline,
        ApplicationConnectionSourceInline,
        ApplicationConnectionTargetInline,
        SCVPermissionInline,
        ReferrerInline,
    ]

class ApplicationFormAdminForm(forms.ModelForm):

    class Meta:
        model = ApplicationForm
        fields = '__all__'

    
class ApplicationConnectionSourceAdminForm(forms.ModelForm):

    class Meta:
        model = ApplicationConnectionSource
        fields = '__all__'
        widgets = {
            'observations': Textarea( attrs={'rows': 1,'cols': 20}),
        }

class ApplicationConnectionSourceAdmin(admin.ModelAdmin):
    form = ApplicationConnectionSourceAdminForm

    
class ApplicationConnectionTargetAdminForm(forms.ModelForm):

    class Meta:
        model = ApplicationConnectionTarget
        fields = '__all__'

class ApplicationConnectionTargetAdmin(admin.ModelAdmin):
    form = ApplicationConnectionTargetAdminForm

    
class SCVPermissionAdminForm(forms.ModelForm):
    permission = forms.ChoiceField(choices = SCVPermission.permissions())

    class Meta:
        model = SCVPermission
        fields = '__all__'

        
class SCVPermissionAdmin(admin.ModelAdmin):
    form = SCVPermissionAdminForm

    
class TestServerAdmin(admin.ModelAdmin):
    exclude = ('signature_date','applicant')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.applicant = request.user.pk
            logging.info("The application server test has been signed by the user %s" \
                         % obj.applicant)
            
        super(TestServerAdmin, self).save_model(request, obj, form, change)


class ProductionServerAdmin(admin.ModelAdmin):
    exclude = ('signature_date','applicant')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.applicant = request.user.pk
            logging.info("The application server production has been signed by the user %s" \
                         % obj.applicant)
            
        super(TestServerAdmin, self).save_model(request, obj, form, change)
        

    
admin.site.register(ApplicationForm,ApplicationFormAdmin)
admin.site.register(ProductionForm)
admin.site.register(Proyect, ProyectAdmin)
#admin.site.register(ApplicationConnectionSource,ApplicationConnectionSourceAdmin)
#admin.site.register(ApplicationConnectionTarget,ApplicationConnectionTargetAdmin)
#admin.site.register(ProductionConnectionTarget)
#admin.site.register(ProductionConnectionSource)
#admin.site.register(ProductionSoftwareRequirement)
#admin.site.register(ApplicationSoftwareRequirement)
admin.site.register(Milestone)
#admin.site.register(Referrer)
admin.site.register(TestServer,TestServerAdmin)
admin.site.register(ProductionServer,ProductionServerAdmin)
#admin.site.register(MonitoredVariable)
#admin.site.register(SCVPermission,SCVPermissionAdmin)
