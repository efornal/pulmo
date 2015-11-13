# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Proyect, ApplicationForm, ApplicationSoftwareRequirement
from .models import ApplicationConnectionSource
from .models import ApplicationConnectionTarget
from .models import SCVPermision, Referrer
from django.utils.translation import ugettext as _
from django.utils import translation
from django.forms import Textarea


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

    class Meta:
        model = ApplicationForm
        #fields = '__all__'
        fields = ('db_name','encoding','user_owner','user_access','observations','proyect')

        
class ApplicationSoftwareRequirementForm(forms.ModelForm):
    name = forms.CharField(max_length=200,required=True)
    version = forms.CharField(max_length=200,required=False)

    class Meta:
        model = ApplicationSoftwareRequirement
        fields = '__all__'


class ApplicationConnectionSourceForm(forms.ModelForm):
    name = forms.CharField(max_length=200,required=True)
    ip = forms.CharField(max_length=200,required=False)
    observations = forms.CharField(required=False, \
                                   widget=forms.Textarea(attrs={'rows':'5', 'cols': '5'}), \
                                   label=_('observations'))
        
    class Meta:
        model = ApplicationConnectionSource
        fields = '__all__'
        widgets = {
            'observations': Textarea( attrs={'rows': 5,'cols': 5}),
        }


class ApplicationConnectionTargetForm(forms.ModelForm):
    name = forms.CharField(max_length=200,required=True)
    ip = forms.CharField(max_length=200,required=False)
    observations = forms.CharField(required=False, label=_('observations'))
        
    class Meta:
        model = ApplicationConnectionTarget
        fields = '__all__'


class SCVPermisionForm(forms.ModelForm):
    user = forms.CharField(max_length=200, required=True, label=_('user'))
    permision = forms.CharField(required=True, label=_('permision'))

    class Meta:
        model = SCVPermision
        fields = '__all__'


class ReferrerForm(forms.ModelForm):
    name   = forms.CharField(max_length=200, required=True, label=_('name'))
    email  = forms.CharField(required=False, label=_('email'))
    phones = forms.CharField(required=False, label=_('phones'))
    is_applicant = forms.BooleanField(required=False, label=_('is_applicant'))
    
    class Meta:
        model = Referrer
        fields = '__all__'
