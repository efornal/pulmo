# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Proyect, ApplicationForm
from django.utils.translation import ugettext as _
from django.utils import translation

class ProyectForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True, label=_('name'))
    description = forms.CharField(required=True, widget=forms.Textarea, label=_('description'))

    class Meta:
        model = Proyect
        fields = ('name', 'description')


class ApplicationFormForm(forms.ModelForm):
    db_name = forms.CharField(max_length=200, required=False)
    encoding = forms.CharField(max_length=200, required=False)
    user_owner  = forms.CharField(max_length=200, required=False)
    user_access = forms.CharField(max_length=200, required=False)
    observations = forms.CharField(required=False, widget=forms.Textarea, label=_('observations'))
#    proyect = forms.ModelChoiceField(queryset=Proyect.objects.all(),
#                                     to_field_name= "proyect",
#                                     required=True, label=_('proyect'))
#    proyect = forms.IntegerField(required=True, label=_('proyect'))


    class Meta:
        model = ApplicationForm
        #fields = '__all__'
        fields = ('db_name','encoding','user_owner','user_access','observations','proyect')
