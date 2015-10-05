from django import forms
from django.contrib import admin
from app.models import Proyect, ApplicationForm, ProductionForm
from app.models import ConnectionTarget, ConnectionSource, SoftwareRequirement
from app.models import Milestone, SCVPermision, Referring, MonitoredVariable

class ProyectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ['name']

#class ApplicationFormAdmin(admin.ModelAdmin):
#    list_display = ('proyect')
#    search_fields = ['proyect']

class SCVPermisionAdminForm(forms.ModelForm):
    permision = forms.ChoiceField(choices = SCVPermision.permisions())

    class Meta:
        model = SCVPermision
        fields = '__all__'

        
class SCVPermisionAdmin(admin.ModelAdmin):
    form = SCVPermisionAdminForm
    
admin.site.register(ApplicationForm)
admin.site.register(ProductionForm)
admin.site.register(Proyect, ProyectAdmin)
admin.site.register(ConnectionTarget)
admin.site.register(ConnectionSource)
admin.site.register(SoftwareRequirement)
admin.site.register(Milestone)
admin.site.register(Referring)
admin.site.register(MonitoredVariable)
admin.site.register(SCVPermision,SCVPermisionAdmin)
