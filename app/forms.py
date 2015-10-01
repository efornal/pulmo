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


# class ApplicationFormForm(forms.ModelForm):
#     observations = forms.CharField(required=True, widget=forms.Textarea, label=_('observations'))
#     encoding = forms.CharField(max_length=200, required=True)

#     class Meta:
#         model = ApplicationForm
#         fields = ('encoding', 'observations')
