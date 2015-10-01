from django.contrib import admin
from app.models import Proyect, ApplicationForm

class ProyectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ['name']

#class ApplicationFormAdmin(admin.ModelAdmin):
#    list_display = ('proyect')
#    search_fields = ['proyect']

admin.site.register(ApplicationForm)
admin.site.register(Proyect, ProyectAdmin)
