from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import logging
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils import translation
from .forms import ProyectForm, ApplicationFormForm, SCVPermisionForm, ReferrerForm
from .forms import ApplicationSoftwareRequirementForm
from .forms import ApplicationConnectionSourceForm, ApplicationConnectionTargetForm
from django.forms.models import inlineformset_factory
from .models import Proyect, ApplicationForm
from django.db import IntegrityError, transaction
from django.forms.models import modelformset_factory



def log_session(request_session):
    # FIXME LOG
    for s in request_session.session.items():
        logging.warning(s)

        
def redirect_without_post(request):
    if request.method != 'POST':
        return redirect('new_step1')

    
def index(request):
    return redirect('new_step1')


def new_step1(request):
    request.session['has_registered'] = False
    request.session['proyect'] = {}
    request.session['application'] = {}
    request.session['sources_computer'] = {}
    request.session['targets_computer'] = {}
    request.session['software'] = {}
    request.session['scv_permisions'] = {}
    request.session['referrers'] = {}
    return render(request, 'new_step1.html')

    
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
        software.append({'name': soft,
                         'version': request.POST.getlist('versions[]')[i] })
    request.session['software'] = software
    request.session.modified = True
    log_session(request)
    return render(request, 'new_step3.html')


def new_step4(request):
    sources_computer = []
    targets_computer = []
    for i,computer in enumerate( request.POST.getlist('sources_name[]') ):
        if computer:
            sources_computer.append({ 'name': computer,
                                      'ip': request.POST.getlist('sources_ip[]')[i],
                                      'observation': request.POST.getlist('sources_observation[]')[i] })
    for i,computer in enumerate( request.POST.getlist('targets_name[]') ):
        if computer:
            targets_computer.append({ 'name': computer,
                                      'ip': request.POST.getlist('targets_ip[]')[i],
                                      'observation': request.POST.getlist('targets_observation[]')[i] })

    request.session['sources_computer'] = sources_computer
    request.session['targets_computer'] = targets_computer
    request.session.modified = True
    log_session(request)
    return render(request, 'new_step4.html')

def new_step5(request):
    permisions = []
    for i,username in enumerate( request.POST.getlist('usernames[]') ):
        if username:
            permisions.append({ 'user': username,
                                      'permision': request.POST.getlist('permisions[]')[i] })

    request.session['scv_permisions'] = permisions
    request.session.modified = True
    log_session(request)
    return render(request, 'new_step5.html')

@transaction.atomic
def save(request):
    redirect_without_post(request)
    referrers = []
    logging.error(request.POST)
    for i,referrer in enumerate( request.POST.getlist('names[]') ):
        if referrer:
            is_applicant = False
            logging.error("%s %s" % (i,len(request.POST.getlist('applicants[]'))))
            if i < len(request.POST.getlist('applicants[]')) and request.POST.getlist('applicants[]')[i]:
                is_applicant = True
                
            referrers.append({ 'name': referrer,
                               'email': request.POST.getlist('emails[]')[i],
                               'phones': request.POST.getlist('phones[]')[i],
                               'is_applicant': is_applicant,
            })

    request.session['referrers'] = referrers
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

            # ac sources 
            for computer in request.session['sources_computer']:
                params = computer.copy()
                params['application_form'] = application.pk
                acs_form =  ApplicationConnectionSourceForm( params )
                if acs_form.is_valid():
                    acs_form.save()
                else:
                    commit_transaction = False
                    logging.error("\n Invalid Application conection source: %s" % acs_form)

            # ac targets
            for computer in request.session['targets_computer']:
                params = computer.copy()
                params['application_form'] = application.pk
                act_form =  ApplicationConnectionTargetForm( params )
                if act_form.is_valid():
                    act_form.save()
                else:
                    commit_transaction = False
                    logging.error("\n Invalid Application conection target: %s" % act_form)

            # scv permisions
            for permision in request.session['scv_permisions']:
                params = permision.copy()
                params['application_form'] = application.pk
                scv_form =  SCVPermisionForm( params )
                if scv_form.is_valid():
                    scv_form.save()
                else:
                    commit_transaction = False
                    logging.error("\n Invalid SCV Permision: %s" % scv_form)

            # referrers
            for referrer in request.session['referrers']:
                params = referrer.copy()
                params['application_form'] = application.pk
                ref_form =  ReferrerForm( params )
                if ref_form.is_valid():
                    ref_form.save()
                else:
                    commit_transaction = False
                    logging.error("\n Invalid Referrer: %s" % ref_form)
                    
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
