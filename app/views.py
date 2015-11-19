# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import logging
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils import translation
from .forms import ProyectForm, ApplicationFormForm, SCVPermissionForm, ReferrerForm
from .forms import SCVPermission
from .forms import ApplicationSoftwareRequirementForm
from .forms import ApplicationConnectionSourceForm, ApplicationConnectionTargetForm
from django.forms.models import inlineformset_factory
from .models import Proyect, ApplicationForm
from django.db import IntegrityError, transaction
from django.forms.models import modelformset_factory
from django.template import Context
from django.shortcuts import render
from django.contrib import messages
 
def log_session(request_session):
    # FIXME LOG
    for s in request_session.session.items():
        logging.warning(s)

        
def redirect_without_post(request):
    if request.method != 'POST':
        return redirect('index')

    
def index(request):
    return redirect('new_step1')


def new_step1(request):
    request.session['has_registered'] = False
    request.session['proyect'] = {}
    request.session['application'] = {}
    request.session['sources_computer'] = {}
    request.session['targets_computer'] = {}
    request.session['software'] = {}
    request.session['scv_permissions'] = {}
    request.session['referrers'] = {}
    return render(request, 'new_step1.html')

    
def new_step2(request):
    redirect_without_post(request)
    
    proyect_form = ProyectForm()
    application_form = ApplicationFormForm()
    context = {'proyect_name': request.POST['name']}

    try:
        proyect_form = ProyectForm(request.POST)
        if proyect_form.is_valid():
            application_form = ApplicationFormForm(request.POST,
                                                   exclude_from_validation='proyect')
            if application_form.is_valid():
                request.session['proyect']['name'] = request.POST['name']
                request.session['proyect']['description'] = request.POST['description']
                request.session['application']['db_name'] = request.POST['db_name']
                request.session['application']['encoding'] = request.POST['encoding']
                request.session['application']['user_owner'] = request.POST['user_owner']
                request.session['application']['user_access'] = request.POST['user_access']
                request.session['application']['observations'] = request.POST['observations']
                request.session.modified = True
                logging.info(" New application: %s" % application_form)
                return render(request, 'new_step2.html', context)
            else:
                logging.warning("Invalid application: %s" % application_form)
        else:
            logging.warning("Invalid proyect: %s" % proyect_form)
    except Exception as e:
        logging.error('%s' % e)

    log_session(request)
    context.update({'proyect_form': proyect_form, 'application_form': application_form})
    return render(request, 'new_step1.html', context)


def new_step3(request):
    redirect_without_post(request)

    software = []
    software_validated = True
    context = {'proyect_name': request.session['proyect']['name']}

    try:
        for i,soft in enumerate( request.POST.getlist('names[]') ):
            if soft:
                params = {'name': soft,
                          'version': request.POST.getlist('versions[]')[i] }
                soft_form = ApplicationSoftwareRequirementForm( params,
                                                                exclude_from_validation='application_form' )
                if soft_form.is_valid():
                    software.append( params )
                else:
                    logging.warning("Invalid application software requirement: %s" % soft_form )
                    software_validated = False
    except Exception as e:
        logging.error('%s' % e)

    if software_validated:
        request.session['software'] = software
        request.session.modified = True
        return render(request, 'new_step3.html', context)
    else:
        context.update({'form': soft_form})
        return render(request, 'new_step2.html', context)

def new_step4(request):
    redirect_without_post(request)
    permissions_options = SCVPermission.permissions()    
    sources_computer = []
    targets_computer = []
    computers_validated = True
    context = {'proyect_name': request.session['proyect']['name'],
               'permissions_options': permissions_options }

    try:
        for i,computer in enumerate( request.POST.getlist('sources_name[]') ):
            if computer:
                params = { 'name': computer,
                           'ip': request.POST.getlist('sources_ip[]')[i],
                           'observation': request.POST.getlist('sources_observation[]')[i] }
                sources_form = ApplicationConnectionSourceForm( params,
                                                                exclude_from_validation='application_form' )
                if sources_form.is_valid():
                    sources_computer.append( params )
                else:
                    logging.warning("Invalid application connection source: %s" % sources_form )
                    computers_validated = False

        for i,computer in enumerate( request.POST.getlist('targets_name[]') ):
            if computer:
                params = { 'name': computer,
                           'ip': request.POST.getlist('targets_ip[]')[i],
                           'observation': request.POST.getlist('targets_observation[]')[i] }
                targets_form = ApplicationConnectionTargetForm( params,
                                                                exclude_from_validation='application_form' )
                if targets_form.is_valid():
                    targets_computer.append()
                else:
                    logging.warning("Invalid application connection source: %s" % sources_form )
                    computers_validated = False
                    
    except Exception as e:
        logging.error('%s' % e)

    if computers_validated:
        request.session['sources_computer'] = sources_computer
        request.session['targets_computer'] = targets_computer
        request.session.modified = True
        log_session(request)
        return render(request, 'new_step4.html', context)
    else:
        context.update({'sources_form': sources_form, 'targets_form': targets_form})
        return render(request, 'new_step3.html', context)

    
def new_step5(request):
    redirect_without_post(request)
    
    permissions = []
    permissions_validated = True
    context = {'proyect_name': request.session['proyect']['name']}
    logging.error( request.POST)
    try:
        for i,username in enumerate( request.POST.getlist('usernames[]') ):
            if username:
                params = { 'user': username,
                           'permission': request.POST.getlist('permissions[]')[i] }
                scv_form =  SCVPermissionForm( params, exclude_from_validation='application_form'  )
                if scv_form.is_valid():
                    permissions.append(params)
                else:
                    logging.warning("Invalid SCV permission: %s" % scv_form )
                    permissions_validated = False
    except Exception as e:
        logging.error('%s' % e)

    if permissions_validated:
        request.session['scv_permissions'] = permissions
        request.session.modified = True
        log_session(request)
        return render(request, 'new_step5.html')
    else:
        context.update({'form': scv_form})
        return render(request, 'new_step4.html', context)


@transaction.atomic
def save(request):
    redirect_without_post(request)
    referrers = []
    ref_validated = True
    logging.error(request.POST)
    context = {'proyect_name': request.session['proyect']['name']}
    
    # validate referrers
    try:
        for i,referrer in enumerate( request.POST.getlist('names[]') ):
            if referrer:
                is_applicant = False
                if i < len(request.POST.getlist('applicants[]')) and request.POST.getlist('applicants[]')[i]:
                    is_applicant = True

                params = { 'name': referrer,
                           'email': request.POST.getlist('emails[]')[i],
                           'phones': request.POST.getlist('phones[]')[i],
                           'is_applicant': is_applicant,
                }
                ref_form =  ReferrerForm( params, exclude_from_validation='application_form' )
                if ref_form.is_valid():
                    referrers.append(params)
                else:
                    logging.warning("Invalid referrer: %s" % ref_form )
                    ref_validated = False
    except Exception as e:
        logging.error('%s' % e)
                
    if ref_validated:
        request.session['referrers'] = referrers
        request.session.modified = True
        log_session(request)
    else:
        context.update({'form': ref_form})
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
            return render(request, 'outcome_success.html', context)
        else:
            transaction.savepoint_rollback( sid )
            
    except IntegrityError:
        logging.error('Integrity error for: %s' % proyect)
        transaction.savepoint_rollback( sid )

    return render(request, 'outcome_error.html.html', context)

