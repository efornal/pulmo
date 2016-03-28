# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import logging
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
from .models import Proyect, ApplicationForm, ProductionForm
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
            msg = "La solicitud se a realizado con éxito. " \
                  "Para completar el trámite te pedimos que te acerques a " \
                  "nuestra oficina con el siguiente formulario impreso y firmado por el solicitante."
            context.update({'application_form_id': application.pk, 'msg': msg,
                            'link_to_application': reverse('print_application_form', args=[application.pk]),
                            'link_to_new_application': reverse('index')})
            return render(request, 'outcome_success.html', context)
        else:
            transaction.savepoint_rollback( sid )
            
    except IntegrityError:
        logging.error('Integrity error for: %s' % proyect)
        transaction.savepoint_rollback( sid )

    msg = "La solicitud no pudo completarse. " \
          "Para poder realizar el trámite te pedimos que te acerques a " \
          "nuestra oficina o intentes realizar la solicitud nuevamente mas tarde.<br>"
    context.update({'msg': msg})
    return render(request, 'outcome_error.html.html', context)

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

def write_header(canvas, doc):
    from reportlab.rl_config import defaultPageSize
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm,inch
    PAGE_HEIGHT=defaultPageSize[1]
    PAGE_WIDTH=defaultPageSize[0]
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
    page = "Pág. %s" % doc.page
    canvas.drawString(PAGE_WIDTH-doc.rightMargin-0.8*inch, PAGE_HEIGHT-doc.topMargin, fecha)
    canvas.drawString(PAGE_WIDTH-doc.rightMargin-0.8*inch, PAGE_HEIGHT-doc.topMargin/1.5, page)
    canvas.restoreState()


def firstPage(canvas, doc):
    write_header(canvas,doc)

def laterPages(canvas, doc):
    write_header(canvas,doc)


def print_application_form (request, proyect_id):

    application = ApplicationForm.objects.get(proyect_id=proyect_id)
    from reportlab.platypus import Paragraph
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm,inch
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
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
    import copy
    styles = getSampleStyleSheet()
    styleH2 =  copy.copy(styles['Heading2'])
    styleN  =  copy.copy(styles['Normal'])
    styleTable = TableStyle([('GRID', (0,1), (-1,-1), 1, colors.black),
                             ('BACKGROUND', (0, 1), (-1, 1), colors.Color(0.9,0.9,0.9)),
                             ('SPAN',(0,0),(0, 0)),])
    space = Spacer(1,0.1*inch)
    space2 = Spacer(1,0.2*inch)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="solicitud.pdf"'
    doc = SimpleDocTemplate(response,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=72)


    content = [space]
    content.append(Paragraph("Formulario Alta de Proyectos", styleH2))
    content.append(space)
    content.append(Paragraph("<b>Nombre del Proyecto</b>: %s" % application.proyect.name or '', styleN))
    content.append(space)
    content.append(Paragraph("<b>Descripcion</b>: %s" % application.proyect.description or '', styleN))
    content.append(space)
    content.append(Paragraph("<b>Nombre DB</b>: %s" % application.db_name or '', styleN))
    content.append(space)
    content.append(Paragraph("<b>Encoding</b>: %s" % application.encoding or '', styleN))
    content.append(space)
    content.append(Paragraph("<b>Usuario owner</b>: %s" % application.user_owner or '', styleN))
    content.append(space)
    content.append(Paragraph("<b>Usuario acceso</b>: %s" % application.user_access or '', styleN))


    data = [['Requerimientos de Software'],['Nombre', 'Versión'],]
    software = ApplicationSoftwareRequirement.objects.filter(application_form=proyect_id)
    if software:
        content.append(space2)
        for item in software:
            data.append( [item.name or '',item.version or ''])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    data = [['Equipos desde los que se conecta'],['Nombre', 'Dirección IP', 'Observaciones'],]
    sources = ApplicationConnectionSource.objects.filter(application_form=proyect_id)
    if sources:
        content.append(space2)
        for item in sources:
            data.append( [item.name or '',item.ip or '', item.observations or ''])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    content.append(space2)
    data = [['Equipos hacia los que se conecta'],['Nombre', 'Dirección IP', 'Observaciones'],]
    targets = ApplicationConnectionTarget.objects.filter(application_form=proyect_id)
    if targets:
        for item in targets:
            data.append( [item.name,item.ip or '', item.observations or ''])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    if application.observations:
        content.append(space2)
        data = [['Observaciones'],]
        data.append([[Paragraph(application.observations or '', styleN)]])
        t = Table(data, colWidths='*')
        t.setStyle(TableStyle([('GRID', (0,1), (-1,-1), 1, colors.Color(0.9,0.9,0.9)),]))
        content.append(t)

    
    data = [['Solicitantes y Referentes'],['Nombre y apellido', 'E-mail', 'Teléfono', 'Es solicitante'],]
    referrers = Referrer.objects.filter(application_form=proyect_id)
    if referrers:
        content.append(space2)
        for item in referrers:
            is_applicant = ""
            if item.is_applicant:
                is_applicant = "Sí"
                data.append( [Paragraph(item.name or '', styleN),
                              Paragraph(item.email or '', styleN),
                              Paragraph(item.phones or '', styleN),
                              Paragraph(is_applicant or '', styleN)])
                t = Table(data, colWidths='*')
                t.setStyle(styleTable)
                content.append(t)


    styleF = copy.copy(styles['Normal'])
    styleF.alignment = TA_RIGHT
    data = [[Paragraph("<br/><br/>%s<br/><br/>%s<br/>%s" % \
                       ("Santa fe, ..... de .......... de 20....",
                        '..................................................',
                        'Firma del solicitante'), styleF)],]
    t = Table(data, colWidths='*')
    t.setStyle(TableStyle([('VALIGN',(-1,-1),(-1,-1),'BOTTOM'),
                           ('ALIGN',(0,0),(0,0),'RIGHT'),]))
    content.append(t)

    doc.build(content, onFirstPage=firstPage, onLaterPages=laterPages, )
    return response




# ========================= views for production ======= \
def print_production_form (request, proyect_id):

    production = ProductionForm.objects.get(proyect_id=proyect_id)
    from reportlab.platypus import Paragraph
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm,inch
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
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
    import copy
    styles = getSampleStyleSheet()
    styleH2 =  copy.copy(styles['Heading2'])
    styleN  =  copy.copy(styles['Normal'])
    styleTable = TableStyle([('GRID', (0,1), (-1,-1), 1, colors.black),
                             ('BACKGROUND', (0, 1), (-1, 1), colors.Color(0.9,0.9,0.9)),
                             ('SPAN',(0,0),(0, 0)),])
    space = Spacer(1,0.1*inch)
    space2 = Spacer(1,0.2*inch)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="solicitud.pdf"'
    doc = SimpleDocTemplate(response,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=72)


    content = [space]
    content.append(Paragraph("Formulario de puesta de servicio en producción", styleH2))
    content.append(space)
    content.append(Paragraph("<b>Nombre del Proyecto</b>: %s" % production.proyect.name or '', styleN))
    content.append(space)
    content.append(Paragraph("<b>Descripcion</b>: %s" % production.proyect.description or '', styleN))
    content.append(space)

    
    if production.observations:
        content.append(space2)
        data = [['Observaciones'],]
        data.append([[Paragraph(production.observations or '', styleN)]])
        t = Table(data, colWidths='*')
        t.setStyle(TableStyle([('GRID', (0,1), (-1,-1), 1, colors.Color(0.9,0.9,0.9)),]))
        content.append(t)

        
    if production.db_name or production.encoding or production.user_owner or production.user_access:
        data = [['Base de datos']]
        content.append(space2)
        data.append(['Nombre','Encoding','Usuario owner', 'Usuario Acceso'])
        data.append([production.db_name or '',
                     production.encoding or '',
                     production.user_owner or '',
                     production.user_access or '',])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

        
    data = [['Volumen de datos estimado'],['','Al inicio', '1er Año', 'Posterior'],]
    content.append(space2)
    if production.db_space_to_start or production.db_space_at_year or production.db_space_after:
        data.append( ['Base de datos',
                      production.db_space_to_start or '',
                      production.db_space_at_year or '',
                      production.db_space_after or ''])
    if production.fs_space_to_start or production.fs_space_at_year or production.fs_space_after:
        data.append( ['Systema de archivos',
                      production.fs_space_to_start or '',
                      production.fs_space_at_year or '',
                      production.fs_space_after or ''])
    t = Table(data, colWidths='*')
    t.setStyle(styleTable)
    content.append(t)

    
    data = [['Requerimientos de hardware'],['','Mínimo', 'Recomendado'],]
    content.append(space2)
    if production.minimum_memory or production.suggested_memory:
        data.append( ['Memoria', production.minimum_memory or '', production.suggested_memory or ''])
    if production.minimum_disk_space or production.suggested_disk_space:
        data.append( ['Disco', production.minimum_disk_space or '', production.suggested_disk_space or ''])
    if production.minimum_processor or production.suggested_processor:
        data.append( ['Procesador', production.minimum_processor or '', production.suggested_processor or ''])
    t = Table(data, colWidths='*')
    t.setStyle(styleTable)
    content.append(t)

            
    data = [['Requerimientos de Software'],['Nombre', 'Versión'],]
    software = ProductionSoftwareRequirement.objects.filter(production_form=proyect_id)
    if software:
        content.append(space2)
        for item in software:
            data.append( [item.name or '',item.version or ''])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    data = [['Equipos desde los que se conecta'],['Nombre', 'Dirección IP', 'Observaciones'],]
    sources = ProductionConnectionSource.objects.filter(production_form=proyect_id)
    if sources:
        content.append(space2)
        for item in sources:
            data.append( [item.name or '',item.ip or '', item.observations or ''])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    content.append(space2)
    data = [['Equipos hacia los que se conecta'],['Nombre', 'Dirección IP', 'Puerto', 'IP Firewall'],]
    targets = ProductionConnectionTarget.objects.filter(production_form=proyect_id)
    if targets:
        for item in targets:
            data.append( [item.name,
                          item.ip or '',
                          item.port or '',
                          item.ip_firewall or ''])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    
    data = [['Variables a monitorizar'],['Variable', 'Periodicidad', 'Conservar historial por'],]
    variables = MonitoredVariable.objects.filter(production_form=proyect_id)
    if variables:
        content.append(space2)
        for item in variables:
            data.append( [Paragraph(item.name or '', styleN),
                          Paragraph(item.periodicity or '', styleN),
                          Paragraph(item.preserving_history_by or '', styleN)])
            t = Table(data, colWidths='*')
            t.setStyle(styleTable)
        content.append(t)

    data = [['Hitos durante el año'],['Hito', 'Fecha', 'Duración en días'],]
    hitos = Milestone.objects.filter(production_form=proyect_id)
    if hitos:
        content.append(space2)
        for item in hitos:
            data.append( [Paragraph(item.description or '', styleN),
                          Paragraph(item.duration or '', styleN),
                          Paragraph(str(item.date_event) or '', styleN)])
            t = Table(data, colWidths='*')
            t.setStyle(styleTable)
        content.append(t)


    styleF = copy.copy(styles['Normal'])
    styleF.alignment = TA_RIGHT
    data = [[Paragraph("<br/><br/>%s<br/><br/>%s<br/>%s" % \
                       ("Santa fe, ..... de .......... de 20....",
                        '..................................................',
                        'Firma del solicitante'), styleF)],]
    t = Table(data, colWidths='*')
    t.setStyle(TableStyle([('VALIGN',(-1,-1),(-1,-1),'BOTTOM'),
                           ('ALIGN',(0,0),(0,0),'RIGHT'),]))
    content.append(t)

    doc.build(content, onFirstPage=firstPage, onLaterPages=laterPages, )
    return response


def redirect_without_production_post(request):
    if request.method != 'POST':
        return redirect('production_step1')

def production_step(request):
    request.session['production_proyect'] = {}
    request.session['production'] = {}
    request.session['production_sources_computer'] = {}
    request.session['production_targets_computer'] = {}
    request.session['production_software'] = {}
    request.session['production_variables']= {}
    request.session['production_milestones']= {}
    proyects = Proyect.without_test_server()
    context = {'proyects': proyects}
    log_session(request)
    return render(request, 'production_step.html', context)
    

def production_step1(request):
    redirect_without_production_post(request)
    
    proyect_id = None
    if 'id' in request.POST:
        proyect_id = request.POST['id'] or None
    if not proyect_id or not Proyect.objects.get(pk=proyect_id):
        logging.warning('Could not determine the project')
        messages.warning(request, 'No se pudo determinar el proyecto sobre el cual realizar la solicitud')
        return redirect('production_step')

    proyect = Proyect.objects.get(pk=proyect_id)    
    proyect_form = ProyectForm(instance=proyect)
    request.session['production_has_registered'] = False
    request.session['production_proyect'] = proyect_id
    request.session.modified = True
    log_session(request)
    context = {'proyect_form': proyect_form }
    return render(request, 'production_step1.html', context)

def production_step2(request):
    redirect_without_production_post(request)
    proyect = Proyect.objects.get(pk=request.session['production_proyect'])    
    proyect_form = ProyectForm(instance=proyect)
    production_form = ProductionFormForm()
    context = {'proyect_form': proyect_form}
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
            log_session(request)
            return render(request, 'production_step2.html', context)
        else:
            logging.warning("Invalid production form: %s" % production_form)
            
    except Exception as e:
        logging.error('%s' % e)

    context.update({'form': production_form,})
    return render(request, 'production_step1.html', context)

def production_step3(request):
    redirect_without_production_post(request)
    log_session(request)
    
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
    log_session(request)
    
    if software_validated:
        return render(request, 'production_step3.html', context)
    else:
        context.update({'form': invalid_form, 'software_list': software})
        return render(request, 'production_step2.html', context)



def production_step4(request):
    redirect_without_production_post(request)

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
                       'observation': request.POST.getlist('sources_observation[]')[i] }
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
    log_session(request)
    
    if computers_validated:
        return render(request, 'production_step4.html', context)
    else:
        context.update({'sources_form': invalid_sources_form, 'targets_form': invalid_targets_form,
                        'sources_computer': sources_computer, 'targets_computer': targets_computer})
        return render(request, 'production_step3.html', context)


def production_step5(request):
    redirect_without_production_post(request)
    
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
    log_session(request)
    
    if variables_validated:
        return render(request, 'production_step5.html', context)
    else:
        context.update({'form': invalid_form, 'variable_list': variables})
        return render(request, 'production_step4.html', context)


@transaction.atomic
def production_step6(request):
    redirect_without_production_post(request)
    
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
                
    if milestone_validate:
        log_session(request) # and continue...
    else:
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
            msg = "La solicitud se a realizado con éxito. " \
                  "Para completar el trámite te pedimos que te acerques a " \
                  "nuestra oficina con el siguiente formulario impreso y firmado por el solicitante."
            context.update({'production_form_id': production.pk, 'msg': msg,
                            'link_to_application': reverse('print_production_form', args=[production.pk] ),
                            'link_to_new_application': reverse('production_step')})
            return render(request, 'outcome_success.html', context)
        else:
            transaction.savepoint_rollback( sid )
            
    except IntegrityError:
        logging.error('Integrity error for: %s' % proyect)
        transaction.savepoint_rollback( sid )

    msg = "La solicitud no pudo completarse. " \
          "Para poder realizar el trámite te pedimos que te acerques a " \
          "nuestra oficina o intentes realizar la solicitud nuevamente mas tarde.<br>"
    context.update({'msg': msg})
    return render(request, 'outcome_error.html.html', context)
