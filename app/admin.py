from django.contrib import admin
from app.models import Proyect

class ProyectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ['name']

admin.site.register(Proyect, ProyectAdmin)
