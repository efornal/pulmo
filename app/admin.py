from django import forms
from django.contrib import admin
from app.models import Proyect, ApplicationForm, ProductionForm, \
    ConnectionTarget, ConnectionSource, ApplicationSoftwareRequirement, ProductionSoftwareRequirement, \
    Milestone, SCVPermision, Referrer, MonitoredVariable, \
    TestServer, ProductionServer


class ProyectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ['name']


class ApplicationSoftwareRequirementInline(admin.TabularInline):
     model = ApplicationSoftwareRequirement
     fk_name = "application_form"

    
class ApplicationFormAdmin(admin.ModelAdmin):
    model = ApplicationForm
    inlines = [
        ApplicationSoftwareRequirementInline,
    ]


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
admin.site.register(ConnectionTarget)
admin.site.register(ConnectionSource)
admin.site.register(ProductionSoftwareRequirement)
admin.site.register(ApplicationSoftwareRequirement)
admin.site.register(Milestone)
admin.site.register(Referrer)
admin.site.register(TestServer)
admin.site.register(ProductionServer)
admin.site.register(MonitoredVariable)
admin.site.register(SCVPermision,SCVPermisionAdmin)
