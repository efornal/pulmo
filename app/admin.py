from django import forms
from django.contrib import admin
from app.models import Proyect, ApplicationForm, ProductionForm
from app.models import ApplicationConnectionTarget, ApplicationConnectionSource
from app.models import ProductionConnectionTarget, ProductionConnectionSource
from app.models import ApplicationSoftwareRequirement, ProductionSoftwareRequirement
from app.models import Milestone, SCVPermision, Referrer, MonitoredVariable
from app.models import TestServer, ProductionServer
from django.forms import ModelForm
from django.forms.widgets import Textarea
from django.db import models


class ProyectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ['name']

class ReferrerInline(admin.TabularInline):
     model = Referrer
     fk_name = "application_form"
     extra = 0

class SCVPermisionInline(admin.TabularInline):
     model = SCVPermision
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
        SCVPermisionInline,
        ReferrerInline,
    ]

    
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

    
class SCVPermisionAdminForm(forms.ModelForm):
    permision = forms.ChoiceField(choices = SCVPermision.permisions())

    class Meta:
        model = SCVPermision
        fields = '__all__'
        
class SCVPermisionAdmin(admin.ModelAdmin):
    form = SCVPermisionAdminForm
    
admin.site.register(ApplicationForm,ApplicationFormAdmin)
admin.site.register(ProductionForm)
admin.site.register(Proyect, ProyectAdmin)
#admin.site.register(ApplicationConnectionSource,ApplicationConnectionSourceAdmin)
#admin.site.register(ApplicationConnectionTarget,ApplicationConnectionTargetAdmin)
admin.site.register(ProductionConnectionTarget)
admin.site.register(ProductionConnectionSource)
admin.site.register(ProductionSoftwareRequirement)
admin.site.register(ApplicationSoftwareRequirement)
admin.site.register(Milestone)
admin.site.register(Referrer)
admin.site.register(TestServer)
admin.site.register(ProductionServer)
admin.site.register(MonitoredVariable)
admin.site.register(SCVPermision,SCVPermisionAdmin)
