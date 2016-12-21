# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import logging
from helpers import to_v, are_all_empty_params
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils import translation
from .forms import ProyectForm, ProductionFormForm
from .forms import ApplicationFormForm, SCVPermissionForm, ReferrerForm
from .forms import SCVPermission
from .forms import ApplicationSoftwareRequirementForm
from .forms import ProductionSoftwareRequirementForm
from .forms import MonitoredVariableForm, MilestoneForm
from .forms import ProductionConnectionSourceForm, ProductionConnectionTargetForm
from .forms import ApplicationConnectionSourceForm, ApplicationConnectionTargetForm
from django.forms.models import inlineformset_factory
from .models import Proyect, ApplicationForm, ProductionForm, TicketSystem
from .models import ApplicationSoftwareRequirement,ProductionSoftwareRequirement, Referrer
from .models import ApplicationConnectionSource, ApplicationConnectionTarget
from .models import ProductionConnectionSource, ProductionConnectionTarget
from .models import MonitoredVariable, Milestone
from django.db import IntegrityError, transaction
from django.forms.models import modelformset_factory
from django.template import Context
from django.shortcuts import render
from django.contrib import messages
from django.core.urlresolvers import reverse
from decorators import redirect_without_post, redirect_if_has_registered
from decorators import redirect_without_production_post,redirect_if_has_production_registered
from zabbix.api import ZabbixAPI
from django.utils import timezone
import json
import subprocess
import re
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def log_session(request_session):
    # FIXME , eliminar
    for s in request_session.session.items():
        logging.info(s)


def defined_as_registered(request):
    request.session['has_registered'] = True
    request.session.modified = True

def instance_info( vm_name='' ):
    result = {} 
    try:
        r = requests.get('{}/{}'.format(settings.GANETI_INSTANCES_URL,vm_name), verify=False)
        if not (r.status_code == requests.codes.ok):
            return ''
        rj = r.json()
        result.update({'vm_proc':rj['beparams']['vcpus']})
        result.update({'vm_disk':rj['disk.sizes'][0]})
        result.update({'vm_cluster':rj['pnode']})
        if 'snodes' in rj and rj['snodes']:
            result.update({'vm_cluster':"{}:{}".format(rj['pnode'],rj['snodes'][0])})
        result.update({'vm_mac':rj['nic.macs'][0]})
        result.update({'vm_ram':rj['beparams']['memory']})
        return result
    except Exception as e:
        logging.error('ERROR Exception: %s' % e)
        return ''

def ip_from_vm_name( vm_name='' ):
    args = ['host',"{}".format(vm_name)]
    try:
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        ip_reg = re.search('[0-9]+.[0-9]+.[0-9]+.[0-9]+', out)
        if ip_reg:
            return ip_reg.group(0)
        else:
            return ''
        
    except Exception as e:
        logging.error('ERROR Exception: %s' % e)
        return ''
    
    
def check_server(request):
    result = {}
    if 'vm_name' in request.POST and request.POST['vm_name']:
        vm_name = request.POST['vm_name']
        logging.info("searching vm name: {}".format(vm_name))

        result.update({'vm_ip': ip_from_vm_name(vm_name)})
        result.update(instance_info(vm_name))
    result_list = json.dumps(result)
    return HttpResponse(result_list)


def define_production_sessions( request ):
    request.session['production_proyect'] = {}
    request.session['production'] = {}
    request.session['production_sources_computer'] = {}
    request.session['production_targets_computer'] = {}
    request.session['production_software'] = {}
    request.session['production_variables']= {}
    request.session['production_milestones']= {}
    request.session.modified = True

    
def unset_production_sessions( request ):
    del request.session['production_proyect']
    del request.session['production']
    del request.session['production_sources_computer']
    del request.session['production_targets_computer']
    del request.session['production_software']
    del request.session['production_variables']
    del request.session['production_milestones']
    request.session.modified = True

    
def unset_application_sessions( request ):
    del request.session['proyect']
    del request.session['application']
    del request.session['sources_computer']
    del request.session['targets_computer']
    del request.session['software']
    del request.session['scv_permissions']
    del request.session['referrers']
    request.session.modified = True

    
def define_application_sessions( request ):
    request.session['has_registered'] = False
    request.session['proyect'] = {}
    request.session['application'] = {}
    request.session['sources_computer'] = {}
    request.session['targets_computer'] = {}
    request.session['software'] = {}
    request.session['scv_permissions'] = {}
    request.session['referrers'] = {}
    request.session.modified = True


@login_required
def index(request):
    if 'HTTP_REFERER' in  request.META \
       and request.META['HTTP_REFERER'] \
       and 'production' in request.META['HTTP_REFERER']:
        return redirect('production_step')
    else:
        return redirect('new_step1')
    

@login_required
def new_step1(request):
    define_application_sessions(request)
    return render(request, 'new_step1.html')


@login_required
@redirect_without_post
def new_step2(request):
    proyect_form = ProyectForm()
    application_form = ApplicationFormForm()
    context = {'proyect_name': request.POST['name']}

    try:
        proyect_form = ProyectForm(request.POST)
        application_form = ApplicationFormForm(request.POST,
                                               exclude_from_validation='proyect')

        if proyect_form.is_valid():
            if application_form.is_valid():
                request.session['proyect']['name'] = request.POST['name']
                request.session['proyect']['secretariat'] = request.POST['secretariat']
                request.session['proyect']['description'] = request.POST['description']
                request.session['application']['db_name'] = request.POST['db_name']
                request.session['application']['encoding'] = request.POST['encoding']
                request.session['application']['user_owner'] = request.POST['user_owner']
                request.session['application']['user_access'] = request.POST['user_access']
                request.session['application']['observations'] = request.POST['observations']
                if 'requires_integration' in request.POST:
                    request.session['application']['requires_integration'] = 1
                else:
                    request.session['application']['requires_integration'] = 0
                request.session['application']['ssh_users'] = request.POST['ssh_users']
                request.session['application']['extra_database_users'] = request.POST['extra_database_users']
                request.session['application']['logs_visualization'] = request.POST['logs_visualization']
                request.session['application']['logs_users'] = request.POST['logs_users']

                request.session.modified = True
                logging.info(" New application: %s" % application_form)
                return render(request, 'new_step2.html', context)
            else:
                logging.warning("Invalid application: %s" % application_form)
        else:
            logging.warning("Invalid proyect: %s" % proyect_form)
    except Exception as e:
        logging.error('%s' % e)

    context.update({'proyect_form': proyect_form, 'application_form': application_form})
    return render(request, 'new_step1.html', context)


@login_required
@redirect_without_post
def new_step3(request):

    software = []
    software_validated = True
    invalid_form = None
    context = {'proyect_name': request.session['proyect']['name']}

    try:
        for i,soft in enumerate( request.POST.getlist('names[]') ):
            params = {'name': soft,
                      'version': request.POST.getlist('versions[]')[i] }
            if not are_all_empty_params(params):
                soft_form = ApplicationSoftwareRequirementForm( params,
                                                                exclude_from_validation='application_form' )
                if soft_form.is_valid():
                    software.append( params )
                else:
                    logging.warning("Invalid application software requirement: %s" % soft_form )
                    software_validated = False
                    invalid_form = soft_form
    except Exception as e:
        logging.error('%s' % e)

    request.session['software'] = software
    request.session.modified = True
    
    if software_validated:
        return render(request, 'new_step3.html', context)
    else:
        context.update({'form': invalid_form, 'software_list': software})
        return render(request, 'new_step2.html', context)

    
@login_required
@redirect_without_post
def new_step4(request):

    permissions_options = SCVPermission.permissions()    
    sources_computer = []
    targets_computer = []
    computers_validated = True
    invalid_sources_form = None
    invalid_targets_form = None
    context = {'proyect_name': request.session['proyect']['name'],
               'permissions_options': permissions_options }

    try:
        for i,computer in enumerate( request.POST.getlist('sources_name[]') ):
            params = { 'name': computer,
                       'ip': request.POST.getlist('sources_ip[]')[i],
                       'service': request.POST.getlist('sources_service[]')[i],
                       'observations': request.POST.getlist('sources_observation[]')[i] }
            if not are_all_empty_params(params):
                sources_form = ApplicationConnectionSourceForm( params,
                                                                exclude_from_validation='application_form' )
                if sources_form.is_valid():
                    sources_computer.append( params )
                else:
                    logging.warning("Invalid application connection source: %s" % sources_form )
                    computers_validated = False
                    invalid_sources_form = sources_form

        for i,computer in enumerate( request.POST.getlist('targets_name[]') ):
            params = { 'name': computer,
                       'ip': request.POST.getlist('targets_ip[]')[i],
                       'service': request.POST.getlist('targets_service[]')[i],
                       'observations': request.POST.getlist('targets_observation[]')[i] }

            if not are_all_empty_params(params):
                targets_form = ApplicationConnectionTargetForm( params,
                                                                exclude_from_validation='application_form' )
                if targets_form.is_valid():
                    targets_computer.append( params )
                else:
                    logging.warning("Invalid application connection source: %s" % sources_form )
                    computers_validated = False
                    invalid_targets_form = targets_form
                
    except Exception as e:
        logging.error('%s' % e)

    request.session['sources_computer'] = sources_computer
    request.session['targets_computer'] = targets_computer
    request.session.modified = True
    
    if computers_validated:
        return render(request, 'new_step4.html', context)
    else:
        context.update({'sources_form': invalid_sources_form, 'targets_form': invalid_targets_form,
                        'sources_computer': sources_computer, 'targets_computer': targets_computer})
        return render(request, 'new_step3.html', context)


@login_required    
@redirect_without_post    
def new_step5(request):

    permissions_options = SCVPermission.permissions()    
    permissions = []
    permissions_validated = True
    invalid_scv_form = None
    context = {'proyect_name': request.session['proyect']['name'],
               'permissions_options': permissions_options }

    try:
        for i,username in enumerate( request.POST.getlist('usernames[]') ):
            params = { 'user': username,
                       'permission': request.POST.getlist('permissions[]')[i] }

            if not are_all_empty_params(params):
                scv_form =  SCVPermissionForm( params, exclude_from_validation='application_form'  )
                if scv_form.is_valid():
                    permissions.append(params)
                else:
                    logging.warning("Invalid SCV permission: %s" % scv_form )
                    invalid_scv_form = scv_form
                    permissions_validated = False
    except Exception as e:
        logging.error('%s' % e)

    request.session['scv_permissions'] = permissions
    request.session.modified = True

    if permissions_validated:
        return render(request, 'new_step5.html', context)
    else:
        context.update({'form': invalid_scv_form, 'permissions_list': permissions})
        return render(request, 'new_step4.html', context)


@login_required
@transaction.atomic
@redirect_without_post
@redirect_if_has_registered
def save(request):
    referrers = []
    ref_validated = True
    invalid_ref_form = None
    context = {'proyect_name': request.session['proyect']['name']}
    
    # validate referrers
    try:
        for i,referrer in enumerate( request.POST.getlist('names[]') ):
            is_applicant = False
            if i < len(request.POST.getlist('applicants[]')) and request.POST.getlist('applicants[]')[i]:
                is_applicant = True

            params = { 'name': referrer,
                       'email': request.POST.getlist('emails[]')[i],
                       'phones': request.POST.getlist('phones[]')[i],
                       'is_applicant': is_applicant,
            }
            if not are_all_empty_params(params):
                ref_form =  ReferrerForm( params, exclude_from_validation='application_form' )
                if ref_form.is_valid():
                    referrers.append(params)
                else:
                    logging.warning("Invalid referrer: %s" % ref_form )
                    ref_validated = False
                    invalid_ref_form = ref_form
    except Exception as e:
        logging.error('%s' % e)

    request.session['referrers'] = referrers
    request.session.modified = True
                
    if not ref_validated:
        context.update({'form': invalid_ref_form, 'referrers_list': referrers})
        return render(request, 'new_step5.html', context)

    
    # === save all data ===
    sid = transaction.savepoint()
    commit_transaction = True
    try:
        proyect_form = ProyectForm(request.session['proyect'])
        if proyect_form.is_valid():
            proyect = proyect_form.save()

            # application form
            app_params = request.session['application']
            app_params['proyect'] = proyect.pk
            application_form = ApplicationFormForm(app_params)
            if application_form.is_valid():
                application = application_form.save()
            else:
                commit_transaction = False
                logging.error("Invalid application: %s" % application_form)

            # requirements software
            for soft in request.session['software']:
                params = soft.copy()
                params['application_form'] = application.pk
                soft_form =  ApplicationSoftwareRequirementForm( params )
                if soft_form.is_valid():
                    soft_form.save()
                else:
                    commit_transaction = False
                    logging.error("Invalid Software Requirements: %s" % soft_form)

            # ac sources 
            for computer in request.session['sources_computer']:
                params = computer.copy()
                params['application_form'] = application.pk
                acs_form =  ApplicationConnectionSourceForm( params )
                if acs_form.is_valid():
                    acs_form.save()
                else:
                    commit_transaction = False
                    logging.error("Invalid Application conection source: %s" % acs_form)

            # ac targets
            for computer in request.session['targets_computer']:
                params = computer.copy()
                params['application_form'] = application.pk
                act_form =  ApplicationConnectionTargetForm( params )
                if act_form.is_valid():
                    act_form.save()
                else:
                    commit_transaction = False
                    logging.error("Invalid Application conection target: %s" % act_form)

            # scv permissions
            for permission in request.session['scv_permissions']:
                params = permission.copy()
                params['application_form'] = application.pk
                scv_form =  SCVPermissionForm( params )
                if scv_form.is_valid():
                    scv_form.save()
                else:
                    commit_transaction = False
                    logging.error("Invalid SCV Permission: %s" % scv_form)

            # referrers
            for referrer in request.session['referrers']:
                params = referrer.copy()
                params['application_form'] = application.pk
                ref_form =  ReferrerForm( params )
                if ref_form.is_valid():
                    ref_form.save()
                else:
                    commit_transaction = False
                    logging.error("Invalid Referrer: %s" % ref_form)
                    
        else:
            commit_transaction = False
            logging.warning("Invalid proyect: %s" % proyect)

        if commit_transaction:
            transaction.savepoint_commit( sid )

            msg = _('completed_application')
            
            if settings.REDMINE_ENABLE_TICKET_CREATION:
                
                    # Main ticket
                    logging.info("Creating main ticket..")
                    emails = Referrer.to_emails_by_application_form(application.pk)
                    watchers = TicketSystem.watchers_ids_by(emails)
                    subject = _('test_server_for') % {'name': application.proyect.name}
                    description = TicketSystem.application_description_issue(application)
                    issue = TicketSystem.create_issue(subject,description,watchers)
                    logging.info('Confirmed ticket request created %s' % issue.id)
                    
                    # Subtask ssh users
                    if application.ssh_users:
                        logging.warning("Creating ticket for SSH users ...")
                        ssh_subject = _('ssh_subject') % {'project_name': application.proyect.name}
                        ssh_description = TicketSystem.ssh_description({'ssh_users':application.ssh_users})
                        ssh_issue = TicketSystem.create_issue(ssh_subject,
                                                              ssh_description,
                                                              None, issue.id)

                    # Subtask extra database users
                    if application.extra_database_users:
                        logging.warning("Creating ticket for extra database users ...")
                        extradb_subject = _('extradb_subject') % {'project_name': application.proyect.name}
                        extradb_description = TicketSystem.extradb_description({'extra_database_users':
                                                                                application.extra_database_users})
                        extradb_issue = TicketSystem.create_issue(extradb_subject,
                                                                  extradb_description,
                                                                  None, issue.id)

                    # Subtask monitoring test
                    logging.warning("Creating ticket for test monitoring ...")
                    monitoring_subject = _('monitoring_subject') % {'project_name': application.proyect.name}
                    monitoring_description = TicketSystem.monitoring_description()
                    monitoring_issue = TicketSystem.create_issue(monitoring_subject,
                                                                 monitoring_description,
                                                                 None, issue.id)

                    # Subtask log level configuration
                    logging.warning("Creating ticket for log level configuration ...")
                    log_subject = _('log_subject') % {'project_name': application.proyect.name}
                    log_description =  TicketSystem.log_description({'logs_visualization': application.logs_visualization,
                                          'logs_users': application.logs_users})
                    log_issue = TicketSystem.create_issue(log_subject,
                                                          log_description,
                                                          None, issue.id)

                    # Subtask integration machine
                    if application.requires_integration:
                        logging.warning("Creating ticket for Integration machine ...")
                        integration_subject = _('integration_subject') % {'project_name': application.proyect.name}
                        integration_description = TicketSystem.integration_description()
                        integration_issue = TicketSystem.create_issue(integration_subject,
                                                              integration_description,
                                                              None, issue.id)
                    
                    issueurl = "%s/issues/%s" % (settings.REDMINE_URL,issue.id)
                    msg += _('confirmed_ticket_request_created') % {'ticket': issue.id,
                                                                    'issueurl': issueurl}
                                                                 
                    application.related_ticket = "#%s" % issue.id
                    application.signature_date = timezone.now()
                    application.received_application = True
                    application.save(update_fields=['related_ticket',
                                                    'signature_date',
                                                    'received_application'])

            context.update({'application_form_id': application.pk, 'msg': msg,
                            'link_to_new_application': reverse('index')})
            unset_application_sessions( request )
            defined_as_registered(request)
            return render(request, 'outcome_success.html', context)
        else:
            transaction.savepoint_rollback( sid )
            
    except IntegrityError:
        logging.error('Integrity error for: %s' % proyect)
        transaction.savepoint_rollback( sid )
    except Exception as e:
        logging.error('ERROR Exception: %s' % e)

    msg = _('incomplete_application')
    context.update({'msg': msg})
    return render(request, 'outcome_error.html', context)


@login_required
def production_step(request):
    define_production_sessions(request)
    proyects = Proyect.production_pass_enabled()
    context = {'proyects': proyects}
    return render(request, 'production_step.html', context)


@login_required
@redirect_without_production_post
def production_step1(request):
    proyect_id = None
    if 'id' in request.POST:
        proyect_id = request.POST['id'] or None
    if not proyect_id or not Proyect.objects.get(pk=proyect_id):
        logging.warning('Could not determine the project')
        messages.warning(request, _('project_not_found'))
        return redirect('production_step')

    proyect = Proyect.objects.get(pk=proyect_id)    
    proyect_form = ProyectForm(instance=proyect)
    request.session['production_has_registered'] = False
    request.session['production_proyect'] = proyect_id
    request.session.modified = True
    context = {'proyect_form': proyect_form }
    return render(request, 'production_step1.html', context)


@login_required
@redirect_without_production_post
def production_step2(request):
    proyect = Proyect.objects.get(pk=request.session['production_proyect'])
    software_in_test = ApplicationSoftwareRequirement.by_proyect(proyect.pk)
    proyect_form = ProyectForm(instance=proyect)
    production_form = ProductionFormForm()
    context = {'proyect_form': proyect_form, 'software_list': software_in_test}
    try:
        params = request.POST.copy()
        params['proyect'] = proyect.pk
        production_form = ProductionFormForm(params)
        if production_form.is_valid():
            request.session['production']['db_name'] = request.POST['db_name']
            request.session['production']['encoding'] = request.POST['encoding']
            request.session['production']['user_owner'] = request.POST['user_owner']
            request.session['production']['user_access'] = request.POST['user_access']
            request.session['production']['observations'] = request.POST['observations']
            request.session['production']['files_backup'] = request.POST['files_backup']
            request.session['production']['db_space_to_start'] = request.POST['db_space_to_start']
            request.session['production']['db_space_at_year'] = request.POST['db_space_at_year']
            request.session['production']['db_space_after'] = request.POST['db_space_after']
            request.session['production']['fs_space_to_start'] = request.POST['fs_space_to_start']
            request.session['production']['fs_space_at_year'] = request.POST['fs_space_at_year']
            request.session['production']['fs_space_after'] = request.POST['fs_space_after']
            request.session['production']['suggested_memory'] = request.POST['suggested_memory']
            request.session['production']['suggested_disk_space'] = request.POST['suggested_disk_space']
            request.session['production']['suggested_processor'] = request.POST['suggested_processor']
            request.session['production']['minimum_memory'] = request.POST['minimum_memory']
            request.session['production']['minimum_disk_space'] = request.POST['minimum_disk_space']
            request.session['production']['minimum_processor'] = request.POST['minimum_processor']
            request.session.modified = True
            return render(request, 'production_step2.html', context)
        else:
            logging.warning("Invalid production form: %s" % production_form)
            
    except Exception as e:
        logging.error('%s' % e)

    context.update({'form': production_form,})
    return render(request, 'production_step1.html', context)


@login_required
@redirect_without_production_post
def production_step3(request):
    proyect = Proyect.objects.get(pk=request.session['production_proyect'])    
    proyect_form = ProyectForm(instance=proyect)
    context = {'proyect_form': proyect_form}
    software = []
    software_validated = True
    invalid_form = None

    try:
        for i,soft in enumerate( request.POST.getlist('names[]') ):
            params = {'name': soft,
                      'version': request.POST.getlist('versions[]')[i] }
            if not are_all_empty_params(params):
                soft_form = ProductionSoftwareRequirementForm( params,
                                                                exclude_from_validation='production_form' )
                if soft_form.is_valid():
                    software.append( params )
                else:
                    logging.warning("Invalid production software requirement: %s" % soft_form )
                    software_validated = False
                    invalid_form = soft_form
    except Exception as e:
        logging.error('%s' % e)

    request.session['production_software'] = software
    request.session.modified = True
    
    if software_validated:
        return render(request, 'production_step3.html', context)
    else:
        context.update({'form': invalid_form, 'software_list': software})
        return render(request, 'production_step2.html', context)


@login_required
@redirect_without_production_post
def production_step4(request):
    proyect = Proyect.objects.get(pk=request.session['production_proyect'])    
    proyect_form = ProyectForm(instance=proyect)
    permissions_options = SCVPermission.permissions()
    context = {'proyect_form': proyect_form, 'permissions_options': permissions_options }

    sources_computer = []
    targets_computer = []
    computers_validated = True
    invalid_sources_form = None
    invalid_targets_form = None

    try:
        for i,computer in enumerate( request.POST.getlist('sources_name[]') ):
            params = { 'name': computer,
                       'ip': request.POST.getlist('sources_ip[]')[i],
                       'username': request.POST.getlist('sources_username[]')[i],
                       'service': request.POST.getlist('sources_service[]')[i],
                       'observations': request.POST.getlist('sources_observation[]')[i] }
            if not are_all_empty_params(params):
                sources_form = ProductionConnectionSourceForm( params,
                                                                exclude_from_validation='production_form' )
                if sources_form.is_valid():
                    sources_computer.append( params )
                else:
                    logging.warning("Invalid production connection source: %s" % sources_form )
                    computers_validated = False
                    invalid_sources_form = sources_form

        for i,computer in enumerate( request.POST.getlist('targets_name[]') ):
            params = { 'name': computer,
                       'ip': request.POST.getlist('targets_ip[]')[i],
                       'username': request.POST.getlist('targets_username[]')[i],
                       'service': request.POST.getlist('targets_service[]')[i],
                       'ip_firewall': request.POST.getlist('targets_ip_firewall[]')[i],
                       'port': request.POST.getlist('targets_port[]')[i] }

            if not are_all_empty_params(params):
                targets_form = ProductionConnectionTargetForm( params,
                                                               exclude_from_validation='production_form' )
                if targets_form.is_valid():
                    targets_computer.append( params )
                else:
                    logging.warning("Invalid production connection target: %s" % targets_form )
                    computers_validated = False
                    invalid_targets_form = targets_form
                
    except Exception as e:
        logging.error('%s' % e)

    request.session['production_sources_computer'] = sources_computer
    request.session['production_targets_computer'] = targets_computer
    request.session.modified = True
    
    if computers_validated:
        return render(request, 'production_step4.html', context)
    else:
        context.update({'sources_form': invalid_sources_form, 'targets_form': invalid_targets_form,
                        'sources_computer': sources_computer, 'targets_computer': targets_computer})
        return render(request, 'production_step3.html', context)


@login_required
@redirect_without_production_post
def production_step5(request):
    proyect = Proyect.objects.get(pk=request.session['production_proyect'])    
    proyect_form = ProyectForm(instance=proyect)
    context = {'proyect_form': proyect_form}
    variables = []
    variables_validated = True
    invalid_form = None

    try:
        for i,variable in enumerate( request.POST.getlist('names[]') ):
            params = {'name': variable,
                      'periodicity': request.POST.getlist('periodicity[]')[i],
                      'preserving_history_by': request.POST.getlist('preserving_history_by[]')[i], }
            if not are_all_empty_params(params):
                variable_form = MonitoredVariableForm( params,
                                                       exclude_from_validation='production_form' )
                if variable_form.is_valid():
                    logging.error(variable_form.is_valid())
                    logging.error(params)
                    variables.append( params )
                else:
                    logging.warning("Invalid production monitored variables: %s" % variable_form )
                    variable_validated = False
                    invalid_form = variable_form
    except Exception as e:
        logging.error('%s' % e)

    request.session['production_variables'] = variables
    request.session.modified = True
    
    if variables_validated:
        return render(request, 'production_step5.html', context)
    else:
        context.update({'form': invalid_form, 'variable_list': variables})
        return render(request, 'production_step4.html', context)


@login_required
@transaction.atomic
@redirect_without_production_post
@redirect_if_has_production_registered
def production_step6(request):
    milestones = []
    milestone_validate = True
    invalid_milestone_form = None
    proyect = Proyect.objects.get(pk=request.session['production_proyect'])    
    proyect_form = ProyectForm(instance=proyect)
    context = {'proyect_form': proyect_form}
    
    # validate milestons
    try:
        for i,milestone in enumerate( request.POST.getlist('descriptions[]') ):
            params = { 'description': milestone,
                       'duration': request.POST.getlist('durations[]')[i],
                       'date_event': request.POST.getlist('date_events[]')[i],
            }
            if not are_all_empty_params(params):
                milestone_form =  MilestoneForm( params, exclude_from_validation='production_form' )
                if milestone_form.is_valid():
                    milestones.append(params)
                else:
                    logging.warning("Invalid milestone: %s" % milestone_form )
                    milestone_validate = False
                    invalid_milestone_form = milestone_form
    except Exception as e:
        logging.error('%s' % e)

    request.session['milestones'] = milestones
    request.session.modified = True
                
    if not milestone_validate:
        context.update({'form': invalid_milestone_form, 'milestones_list': milestones})
        return render(request, 'production_step5.html', context)

    
    # === save all data ===
    sid = transaction.savepoint()
    commit_transaction = True
    try:
        # produciton form
        produciton_params = request.session['production']
        produciton_params['proyect'] = proyect.pk
        production_form = ProductionFormForm(produciton_params)

        if production_form.is_valid():
            production = production_form.save()
        else:
            commit_transaction = False
            logging.error("Invalid production: %s" % production_form)

        # requirements software
        for soft in request.session['production_software']:
            params = soft.copy()
            params['production_form'] = production.pk
            soft_form =  ProductionSoftwareRequirementForm( params )
            if soft_form.is_valid():
                soft_form.save()
            else:
                commit_transaction = False
                logging.error("Invalid Software Requirements: %s" % soft_form)

        # ac sources 
        for computer in request.session['production_sources_computer']:
            params = computer.copy()
            params['production_form'] = production.pk
            acs_form =  ProductionConnectionSourceForm( params )
            if acs_form.is_valid():
                acs_form.save()
            else:
                commit_transaction = False
                logging.error("Invalid Production conection source: %s" % acs_form)

        # ac targets
        for computer in request.session['production_targets_computer']:
            params = computer.copy()
            params['production_form'] = production.pk
            act_form =  ProductionConnectionTargetForm( params )
            if act_form.is_valid():
                act_form.save()
            else:
                commit_transaction = False
                logging.error("Invalid Production conection target: %s" % act_form)

        # variables
        for variable in request.session['production_variables']:
            params = variable.copy()
            params['production_form'] = production.pk
            variable_form =   MonitoredVariableForm( params )
            if variable_form.is_valid():
                variable_form.save()
            else:
                commit_transaction = False
                logging.error("Invalid monitored Variable: %s" % variable_form)

        # referrers
        for milestone in request.session['milestones']:
            params = milestone.copy()
            params['production_form'] = production.pk
            milestone_form =  MilestoneForm( params )
            if milestone_form.is_valid():
                milestone_form.save()
            else:
                commit_transaction = False
                logging.error("Invalid Milestone: %s" % milestone_form)
                    

        if commit_transaction:
            transaction.savepoint_commit( sid )
            
            msg = _('completed_application')
            
            if settings.REDMINE_ENABLE_TICKET_CREATION:
                # se debe crear ticket
                watcher = TicketSystem.watchers_ids_by([production.applicant])
                subject = _('production_server_for') % {'name': production.proyect.name}
                description = TicketSystem.production_description_issue(production)
                issue = TicketSystem.create_issue(subject,description,watcher)
                logging.info('Confirmed ticket request created %s' % issue.id)

                monitoring_subject=_('add_to_monitoring') % {'name': production.proyect.name}
                monitoring_description = _('add_to_monitoring_desc')
                monitoring_issue = TicketSystem.create_issue(monitoring_subject,
                                                             monitoring_description,
                                                             None,
                                                             issue.id)
                backup_subject=_('add_to_backup') % {'name': production.proyect.name}
                backup_description = _('add_to_backup_desc')
                backup_issue = TicketSystem.create_issue(backup_subject,
                                                         backup_description,
                                                         None,
                                                         issue.id)

                issueurl = "%s/issues/%s" % (settings.REDMINE_URL,issue.id)
                msg += _('confirmed_ticket_request_created') % {'ticket': issue.id,
                                                                'issueurl': issueurl}
                                                                 
                production.related_ticket = "#%s" % issue.id
                production.signature_date = timezone.now()
                production.received_application = True
                production.save(update_fields=['related_ticket',
                                               'signature_date',
                                               'received_application'])

            context.update({'production_form_id': production.pk, 'msg': msg,
                            'link_to_new_application': reverse('production_step')})
            unset_production_sessions( request )
            defined_as_registered(request)
            return render(request, 'outcome_success.html', context)
        else:
            transaction.savepoint_rollback( sid )
            
    except IntegrityError:
        logging.error('Integrity error for: %s' % proyect)
        transaction.savepoint_rollback( sid )
    except Exception as e:
        logging.error('ERROR Exception: %s' % e)
        
    msg = _('incomplete_application')
    context.update({'msg': msg})
    return render(request, 'outcome_error.html', context)
