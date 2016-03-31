# -*- encoding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import Proyect, ApplicationForm, ProductionForm, ApplicationSoftwareRequirement
from .models import ProductionSoftwareRequirement
from .models import MonitoredVariable
from .models import Milestone, TestServer, ProductionServer
from .models import ApplicationConnectionSource, ApplicationConnectionTarget
from .models import ProductionConnectionSource, ProductionConnectionTarget
from .models import SCVPermission, Referrer
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
    
    def __init__(self,*args,**kwargs):
        field_to_exclude = ''
        if kwargs.get('exclude_from_validation', False):
            field_to_exclude = kwargs.pop('exclude_from_validation')
        super(ApplicationFormForm, self).__init__(*args,**kwargs)
        if field_to_exclude:
            self.fields.pop(field_to_exclude)
        
    class Meta:
        model = ApplicationForm
        fields = '__all__'
        #fields = ('db_name','encoding','user_owner','user_access','observations', 'application_form')

        
class ApplicationSoftwareRequirementForm(forms.ModelForm):
    name = forms.CharField(max_length=200,required=True)
    version = forms.CharField(max_length=200,required=False)

    def __init__(self,*args,**kwargs):
        field_to_exclude = ''
        if kwargs.get('exclude_from_validation', False):
            field_to_exclude = kwargs.pop('exclude_from_validation')
        super(ApplicationSoftwareRequirementForm, self).__init__(*args,**kwargs)
        if field_to_exclude:
            self.fields.pop(field_to_exclude)
     
    class Meta:
        model = ApplicationSoftwareRequirement
        fields = '__all__'


class ProductionSoftwareRequirementForm(forms.ModelForm):
    name = forms.CharField(max_length=200,required=True)
    version = forms.CharField(max_length=200,required=False)

    def __init__(self,*args,**kwargs):
        field_to_exclude = ''
        if kwargs.get('exclude_from_validation', False):
            field_to_exclude = kwargs.pop('exclude_from_validation')
        super(ProductionSoftwareRequirementForm, self).__init__(*args,**kwargs)
        if field_to_exclude:
            self.fields.pop(field_to_exclude)
     
    class Meta:
        model = ProductionSoftwareRequirement
        fields = '__all__'


class ApplicationConnectionSourceForm(forms.ModelForm):
    name = forms.CharField(max_length=200,required=True)
    ip = forms.CharField(max_length=200,required=False)
    observations = forms.CharField(required=False, \
                                   widget=forms.Textarea(attrs={'rows':'5', 'cols': '5'}), \
                                   label=_('observations'))

    def __init__(self,*args,**kwargs):
        field_to_exclude = ''
        if kwargs.get('exclude_from_validation', False):
            field_to_exclude = kwargs.pop('exclude_from_validation')
        super(ApplicationConnectionSourceForm, self).__init__(*args,**kwargs)
        if field_to_exclude:
            self.fields.pop(field_to_exclude)
        
    class Meta:
        model = ApplicationConnectionSource
        fields = '__all__'
        widgets = {
            'observations': Textarea( attrs={'rows': 5,'cols': 5}),
        }

class ProductionConnectionSourceForm(forms.ModelForm):
    name = forms.CharField(max_length=200,required=True)
    ip = forms.CharField(max_length=200,required=False)
    observations = forms.CharField(required=False, \
                                   widget=forms.Textarea(attrs={'rows':'5', 'cols': '5'}), \
                                   label=_('observations'))

    def __init__(self,*args,**kwargs):
        field_to_exclude = ''
        if kwargs.get('exclude_from_validation', False):
            field_to_exclude = kwargs.pop('exclude_from_validation')
        super(ProductionConnectionSourceForm, self).__init__(*args,**kwargs)
        if field_to_exclude:
            self.fields.pop(field_to_exclude)
        
    class Meta:
        model = ProductionConnectionSource
        fields = '__all__'
        widgets = {
            'observations': Textarea( attrs={'rows': 5,'cols': 5}),
        }
        

class ApplicationConnectionTargetForm(forms.ModelForm):
    name = forms.CharField(max_length=200,required=True)
    ip = forms.CharField(max_length=200,required=False)
    observations = forms.CharField(required=False, label=_('observations'))

    def __init__(self,*args,**kwargs):
        field_to_exclude = ''
        if kwargs.get('exclude_from_validation', False):
            field_to_exclude = kwargs.pop('exclude_from_validation')
        super(ApplicationConnectionTargetForm, self).__init__(*args,**kwargs)
        if field_to_exclude:
            self.fields.pop(field_to_exclude)
        
    class Meta:
        model = ApplicationConnectionTarget
        fields = '__all__'


class ProductionConnectionTargetForm(forms.ModelForm):
    name = forms.CharField(max_length=200,required=True)
    ip = forms.CharField(max_length=200,required=False)
    ip_firewall = forms.CharField(max_length=200,required=False)
    port = forms.CharField(required=False, label=_('port'))

    def __init__(self,*args,**kwargs):
        field_to_exclude = ''
        if kwargs.get('exclude_from_validation', False):
            field_to_exclude = kwargs.pop('exclude_from_validation')
        super(ProductionConnectionTargetForm, self).__init__(*args,**kwargs)
        if field_to_exclude:
            self.fields.pop(field_to_exclude)
        
    class Meta:
        model = ProductionConnectionTarget
        fields = '__all__'


        
class SCVPermissionForm(forms.ModelForm):
    user = forms.CharField(max_length=200, required=True, label=_('user'))
    permission = forms.CharField(required=True, label=_('permission'))

    def __init__(self,*args,**kwargs):
        field_to_exclude = ''
        if kwargs.get('exclude_from_validation', False):
            field_to_exclude = kwargs.pop('exclude_from_validation')
        super(SCVPermissionForm, self).__init__(*args,**kwargs)
        if field_to_exclude:
            self.fields.pop(field_to_exclude)

    class Meta:
        model = SCVPermission
        fields = '__all__'

        
class MonitoredVariableForm(forms.ModelForm):
    name = forms.CharField(max_length=200, required=True, label=_('user'))
    periodicity = forms.CharField(required=True, label=_('permission'))
    preserving_history_by = forms.CharField(max_length=200,required=False, label=_('preserving_history_by'))

    def __init__(self,*args,**kwargs):
        field_to_exclude = ''
        if kwargs.get('exclude_from_validation', False):
            field_to_exclude = kwargs.pop('exclude_from_validation')
        super(MonitoredVariableForm, self).__init__(*args,**kwargs)
        if field_to_exclude:
            self.fields.pop(field_to_exclude)

    class Meta:
        model = MonitoredVariable
        fields = '__all__'

        
class ReferrerForm(forms.ModelForm):
    name   = forms.CharField(max_length=200, required=True, label=_('name'))
    email  = forms.CharField(required=False, label=_('email'))
    phones = forms.CharField(required=False, label=_('phones'))
    is_applicant = forms.BooleanField(required=False, label=_('is_applicant'))

    def __init__(self,*args,**kwargs):
        field_to_exclude = ''
        if kwargs.get('exclude_from_validation', False):
            field_to_exclude = kwargs.pop('exclude_from_validation')
        super(ReferrerForm, self).__init__(*args,**kwargs)
        if field_to_exclude:
            self.fields.pop(field_to_exclude)
    
    class Meta:
        model = Referrer
        fields = '__all__'

class MilestoneForm(forms.ModelForm):
    description = forms.CharField(max_length=200, required=True, label=_('description'))
    duration    = forms.CharField(required=False, label=_('duration'))
    date_event  = forms.DateField(required=False, label=_('date_event'))

    def __init__(self,*args,**kwargs):
        field_to_exclude = ''
        if kwargs.get('exclude_from_validation', False):
            field_to_exclude = kwargs.pop('exclude_from_validation')
        super(MilestoneForm, self).__init__(*args,**kwargs)
        if field_to_exclude:
            self.fields.pop(field_to_exclude)
    
    class Meta:
        model = Milestone
        fields = '__all__'
        
        
class ProductionFormForm(forms.ModelForm):
    proyect   = forms.ModelChoiceField(queryset=Proyect.objects.all(),
                                       to_field_name= "id",
                                       required=True,
                                       label=_('proyect'))

    db_name = forms.CharField(max_length=200, required=False)
    encoding = forms.CharField(max_length=200, required=False)
    user_owner  = forms.CharField(max_length=200, required=False)
    user_access = forms.CharField(max_length=200, required=False)
    observations = forms.CharField(required=False, widget=forms.Textarea, label=_('observations'))

    db_space_to_start = forms.CharField(max_length=200, required=False)
    db_space_at_year  = forms.CharField(max_length=200, required=False)
    db_space_after    = forms.CharField(max_length=200, required=False)

    fs_space_to_start = forms.CharField(max_length=200, required=False)
    fs_space_at_year  = forms.CharField(max_length=200, required=False)
    fs_space_after    = forms.CharField(max_length=200, required=False)

    minimum_memory = forms.CharField(max_length=200, required=False)
    minimum_disk_space = forms.CharField(max_length=200, required=False)
    minimum_processor = forms.CharField(max_length=200, required=False)

    suggested_memory = forms.CharField(max_length=200, required=False)
    suggested_disk_space = forms.CharField(max_length=200, required=False)
    suggested_processor = forms.CharField(max_length=200, required=False)

    files_backup = forms.CharField(required=False)

    class Meta:
        model = ProductionForm
        fields = '__all__'
        #fields = ('db_name','encoding','user_owner','user_access','observations', 'production_form')
        

class TestServerForm(forms.ModelForm):
    class Meta:
        model = TestServer
        fields = '__all__'
