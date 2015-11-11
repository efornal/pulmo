from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import logging
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils import translation
from .forms import ProyectForm, ApplicationFormForm, ApplicationSoftwareRequirementForm
from django.forms.models import inlineformset_factory
from .models import Proyect, ApplicationForm
from django.db import IntegrityError, transaction
from django.forms.models import modelformset_factory

def index(request):
    return redirect('new_step1')

def new_step1(request):
    request.session['has_registered'] = False
    request.session['proyect'] = {}
    request.session['application'] = {}
    request.session['computers'] = {}
    request.session['software'] = {}
    request.session['scv'] = {}
    request.session['referrer'] = {}
    return render(request, 'new_step1.html')

def log_session(request_session):
    # FIXME LOG
    for s in request_session.session.items():
        logging.warning(s)

def redirect_without_post(request):
    if request.method != 'POST':
        return redirect('new_step1')
    
@transaction.atomic
def new_step2(request):
    # FIXME: example for validations!
    context = {}
    proyect_form = ProyectForm()
    application_form = ApplicationFormForm()
    
    redirect_without_post(request)
    
    sid = transaction.savepoint()
    try:
        proyect_form = ProyectForm(request.POST)
        if proyect_form.is_valid():
            proyect = proyect_form.save()
            app_params = request.POST.copy()
            app_params['proyect'] = proyect.id
            application_form = ApplicationFormForm(app_params)
            if application_form.is_valid():
                request.session['proyect']['name'] = request.POST['name']
                request.session['proyect']['description'] = request.POST['description']
                request.session['application']['db_name'] = request.POST['db_name']
                request.session['application']['encoding'] = request.POST['encoding']
                request.session['application']['user_owner'] = request.POST['user_owner']
                request.session['application']['user_access'] = request.POST['user_access']
                request.session['application']['observations'] = request.POST['observations']
                request.session.modified = True
                logging.warning("\n New application: %s" % application_form)
                return render(request, 'new_step2.html')
            else:
                logging.warning("\nInvalid application: %s" % application_form)
        else:
            logging.warning("\nInvalid proyect: %s\n" % proyect_form)
    except IntegrityError:
        logging.error('\nIntegrity error for: %s\n' % proyect)
    finally:  # mandatory rollback,.. FIXME! refactor validations!!
        transaction.savepoint_rollback( sid )
    log_session(request)
    context = {'proyect_form': proyect_form, 'application_form': application_form}
    return render(request, 'new_step1.html', context)


def new_step3(request):
    software = []
    for i,soft in enumerate( request.POST.getlist('names[]') ):
        software.append({'name': soft, 'version': request.POST.getlist('versions[]')[i]})
    request.session['software'] = software
    request.session.modified = True
    log_session(request)
    return render(request, 'new_step3.html')


def new_step4(request):
    request.session['computers']['names'] = request.POST.getlist('names[]')
    request.session['computers']['ips'] = request.POST.getlist('ips[]')
    request.session['computers']['observations'] = request.POST.getlist('observations[]')
    request.session.modified = True
    log_session(request)
    return render(request, 'new_step4.html')

def new_step5(request):
    request.session['scv']['usernames'] = request.POST.getlist('usernames[]')
    request.session['scv']['permisions'] = request.POST.getlist('permisions[]')
    request.session.modified = True
    log_session(request)
    return render(request, 'new_step5.html')

@transaction.atomic
def save(request):
    redirect_without_post(request)
    request.session['referrer']['names'] = request.POST.getlist('names[]')
    request.session['referrer']['emails'] = request.POST.getlist('emails[]')
    request.session['referrer']['phones'] = request.POST.getlist('phones[]')
    request.session['referrer']['applicants'] = request.POST.getlist('applicants[]')
    request.session.modified = True
    log_session(request)
    
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
                logging.error(" \n Invalid application: %s\n" % application_form)

            # requirements software
            for soft in request.session['software']:
                params = soft.copy()
                params['application_form'] = application.pk
                soft_form =  ApplicationSoftwareRequirementForm( params )
                if soft_form.is_valid():
                    soft_form.save()
                else:
                    commit_transaction = False
                    logging.error("\n Invalid Software Requirements: %s" % soft_form)
                    
        else:
            commit_transaction = False
            logging.warning("\n Invalid proyect: %s\n" % proyect)

        if commit_transaction:
            transaction.savepoint_commit( sid )
        else:
            transaction.savepoint_rollback( sid )
            
    except IntegrityError:
        logging.error('\nIntegrity error for: %s\n' % proyect)
        transaction.savepoint_rollback( sid )
        

    return HttpResponse("Values: %s" % proyect )
