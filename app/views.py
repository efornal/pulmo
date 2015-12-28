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

def are_all_empty_params( params ):
    for key,value in params.iteritems():
        if value:
            return False
    return True
        
def redirect_without_post(request):
    if request.method != 'POST':
        return redirect('index')

    
def index(request):
    #return redirect('new_step1')
    return print_form()
    

    
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
    log_session(request)
    
    if software_validated:
        return render(request, 'new_step3.html', context)
    else:
        context.update({'form': invalid_form, 'software_list': software})
        return render(request, 'new_step2.html', context)

def new_step4(request):
    redirect_without_post(request)

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
                       'observation': request.POST.getlist('sources_observation[]')[i] }
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
                       'observation': request.POST.getlist('targets_observation[]')[i] }

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
    log_session(request)
    
    if computers_validated:
        return render(request, 'new_step4.html', context)
    else:
        context.update({'sources_form': invalid_sources_form, 'targets_form': invalid_targets_form,
                        'sources_computer': sources_computer, 'targets_computer': targets_computer})
        return render(request, 'new_step3.html', context)

    
def new_step5(request):
    redirect_without_post(request)

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
    log_session(request)

    if permissions_validated:
        return render(request, 'new_step5.html', context)
    else:
        context.update({'form': invalid_scv_form, 'permissions_list': permissions})
        return render(request, 'new_step4.html', context)


@transaction.atomic
def save(request):
    redirect_without_post(request)
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
                
    if ref_validated:
        log_session(request) # and continue...
    else:
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
            return render(request, 'outcome_success.html', context)
        else:
            transaction.savepoint_rollback( sid )
            
    except IntegrityError:
        logging.error('Integrity error for: %s' % proyect)
        transaction.savepoint_rollback( sid )

    return render(request, 'outcome_error.html.html', context)


def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    styles = getSampleStyleSheet()
 
    # Header
    header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
    w, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
 
    # Footer
    footer = Paragraph('This is a multi-line footer.  It goes on every page.   ' * 5, styles['Normal'])
    w, h = footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, h)
 
    # Release the canvas
    canvas.restoreState()

def parag_style():
    from  reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    style = ParagraphStyle('test')
    style.textColor = 'black'
    style.borderColor = 'black'
    style.borderWidth = 0
    style.alignment = TA_LEFT
    style.fontSize = 9
    return style

from reportlab.rl_config import defaultPageSize
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm,inch
PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]


def write_header(canvas, doc):
    from django.conf import settings
    from reportlab.platypus import Paragraph
    from reportlab.lib.units import cm
    from datetime import datetime
    canvas.saveState()
    fecha = datetime.now().strftime("%d/%m/%y %H:%M")
    if settings.STATIC_ROOT:
        img_path = "%s/images/logo.png" % settings.STATIC_ROOT
    else:
        img_path = "%s%simages/logo.png" % (settings.BASE_DIR,settings.STATIC_URL)
    canvas.drawImage(img_path,doc.leftMargin , PAGE_HEIGHT-doc.topMargin, 1.5*cm, 1.5*cm)
    canvas.line( doc.leftMargin , PAGE_HEIGHT-1.05*doc.topMargin,
                 PAGE_WIDTH-doc.rightMargin,PAGE_HEIGHT-1.05*doc.topMargin)
    parag = Paragraph("Dirección de Informatización" \
                      "<br/>Rectorado<br/>Universidad Nacional",parag_style())
    parag.wrapOn(canvas,PAGE_WIDTH*0.5, PAGE_HEIGHT)
    parag.drawOn(canvas, 2*doc.leftMargin , PAGE_HEIGHT-doc.topMargin)
    canvas.setFont('Times-Roman',9)
    canvas.drawString(PAGE_WIDTH-doc.rightMargin-0.8*inch, PAGE_HEIGHT-doc.topMargin, fecha)
    canvas.restoreState()

def firstPage(canvas, doc):
    write_header(canvas,doc)
    
def laterPages(canvas, doc):
    write_header(canvas,doc)
    
def print_form():
    from reportlab.platypus import Paragraph
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm,inch
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus.flowables import Spacer, Flowable
    from io import BytesIO
    from django.http import HttpResponse
    from django.views.generic import ListView
    from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import Table, Image
    from reportlab.pdfgen import canvas
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="solicitud.pdf"'
    doc = SimpleDocTemplate(response,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=72)

    styles = getSampleStyleSheet()
    content = [Spacer(1,0.2*inch)]    
    content.append(Paragraph("Formulario Alta de Proyectos",  styles['Heading2']))
    content.append(Spacer(1,0.1*inch))
    content.append(Paragraph("Nombre del Proyecto:", styles['Normal']))
    content.append(Spacer(1,0.1*inch))
    content.append(Paragraph("Descripción:", styles['Normal']))
    content.append(Spacer(1,0.1*inch))
    content.append(Paragraph("Nombre DB:", styles['Normal']))
    content.append(Spacer(1,0.1*inch))
    content.append(Paragraph("Encoding:", styles['Normal']))
    content.append(Spacer(1,0.1*inch))
    content.append(Paragraph("Usuario owner:", styles['Normal']))
    content.append(Spacer(1,0.1*inch))
    content.append(Paragraph("Usuario acceso:", styles['Normal']))

    content.append(Spacer(1,0.2*inch))
    data= [['Requerimientos de Software'],['Nombre', 'Versión'],
           ['Apache','2.0']]
    t = Table(data)
    t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black),]))

    content.append(t)

    doc.build(content, onFirstPage=firstPage, onLaterPages=laterPages)
    return response




