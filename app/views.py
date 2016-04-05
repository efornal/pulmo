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
            msg = _('completed_application')
            context.update({'application_form_id': application.pk, 'msg': msg,
                            'link_to_application': reverse('print_application_form', args=[application.pk]),
                            'link_to_new_application': reverse('index')})
            return render(request, 'outcome_success.html', context)
        else:
            transaction.savepoint_rollback( sid )
            
    except IntegrityError:
        logging.error('Integrity error for: %s' % proyect)
        transaction.savepoint_rollback( sid )

    msg = _('incomplete_application')
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
    style.fontSize = 8
    return style
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        from reportlab.rl_config import defaultPageSize
        from reportlab.lib.units import cm
        PAGE_HEIGHT=defaultPageSize[1]
        PAGE_WIDTH=defaultPageSize[0]

        page = "Pág. %s of %s" % (self._pageNumber, page_count)
        self.setFont('Times-Roman',8)
        self.drawString(PAGE_WIDTH-3.9*cm, PAGE_HEIGHT-1.6*cm, page)

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
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    if settings.STATIC_ROOT:
        img_path = "%s/images/logo_header.png" % settings.STATIC_ROOT
    else:
        img_path = "%s%simages/logo_header.png" % (settings.BASE_DIR,settings.STATIC_URL)
    canvas.drawImage(img_path,doc.leftMargin+0.1*cm , PAGE_HEIGHT-doc.topMargin, 1.3*cm, 1.3*cm)
    canvas.line( doc.leftMargin+0.1*cm , PAGE_HEIGHT-1.05*doc.topMargin,
                 PAGE_WIDTH-1.05*doc.rightMargin,PAGE_HEIGHT-1.05*doc.topMargin)
    parag = Paragraph( _('header_text') ,parag_style())
    parag.wrapOn(canvas,PAGE_WIDTH*0.5, PAGE_HEIGHT)
    parag.drawOn(canvas, 1.6*doc.leftMargin , PAGE_HEIGHT-doc.topMargin)
    canvas.setFont('Times-Roman',8)
    canvas.drawString(PAGE_WIDTH-doc.rightMargin-0.85*inch, PAGE_HEIGHT-doc.topMargin, fecha)
    canvas.restoreState()


def firstPage(canvas, doc):
    write_header(canvas,doc)

def laterPages(canvas, doc):
    write_header(canvas,doc)

def to_c( field_name ):
    return "<b>%s</b>" % field_name

def to_v( field_value ):
    return field_value or ''

def to_cv( field_name, field_value ):
    return "%s: %s" % ( to_c(field_name), to_v(field_value) )

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
    styleH5 =  copy.copy(styles['Heading5'])
    styleN  =  copy.copy(styles['Normal'])
    styleN.fontSize = 8
    styleTable = TableStyle([('GRID', (0,1), (-1,-1), 1, colors.black),
                             ('FONTSIZE', (0, 0), (-1, -1), 8), 
                             ('BACKGROUND', (0, 1), (-1, 1), colors.Color(0.9,0.9,0.9)),
                             ('SPAN',(0,0),(0, 0)),])
    styleTableObs = TableStyle([('GRID', (0,1), (-1,-1), 1, colors.Color(0.9,0.9,0.9)),
                                ('FONTSIZE', (0, 0), (-1, -1), 8),])
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
    content.append(Paragraph( _('subscription_application_form') , styleH5))
    content.append(space)
    content.append(Paragraph(to_cv(_('proyect_name'), application.proyect.name), styleN ))

    if application.proyect.description:
        content.append(space)
        data = [[_('description')],]
        data.append([[Paragraph(to_v(application.proyect.description), styleN)]])
        t = Table(data, colWidths='*')
        t.setStyle(styleTableObs)
        content.append(t)

    if application.observations:
        content.append(space)
        data = [[_('observations')],]
        data.append([[Paragraph(to_v(application.observations), styleN)]])
        t = Table(data, colWidths='*')
        t.setStyle(styleTableObs)
        content.append(t)
        
    if application.db_name or application.encoding or application.user_owner or application.user_access:
        data = [[_('database')]]
        content.append(space)
        data.append([_('name'),_('encoding'),_('user_owner'),_('user_access')])
        data.append([to_v(application.db_name),
                     to_v(application.encoding),
                     to_v(application.user_owner),
                     to_v(application.user_access),])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)


    software = ApplicationSoftwareRequirement.objects.filter(application_form=proyect_id)
    if software:
        data = [[_('software_requirements')],[_('name'),_('version')],]
        content.append(space)
        for item in software:
            data.append( [to_v(item.name),to_v(item.version)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    sources = ApplicationConnectionSource.objects.filter(application_form=proyect_id)
    if sources:
        data = [[_('connection_sources')],[_('name'),_('ip_address'),_('service'),_('observations')],]
        content.append(space)
        for item in sources:
            data.append( [to_v(item.name),to_v(item.ip),to_v(item.service),to_v(item.observations)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    targets = ApplicationConnectionTarget.objects.filter(application_form=proyect_id)
    if targets:
        content.append(space)
        data = [[_('connection_targets')],[_('name'),_('ip_address'),_('service'),_('observations')],]
        for item in targets:
            data.append( [to_v(item.name),to_v(item.ip),to_v(item.service),to_v(item.observations)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    csv_permission = SCVPermission.objects.filter(application_form=proyect_id)
    if csv_permission:
        data = [[_('vcs_repository')],[_('users'),_('permissions')],]
        content.append(space)
        for item in csv_permission:
            data.append( [to_v(item.user),to_v(item.permission)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)
    

    referrers = Referrer.objects.filter(application_form=proyect_id)
    if referrers:
        data = [[_('applicants_and_referentes')],
                [_('name_and_surname'),_('email'),_('phones'),_('is_applicant')],]
        content.append(space)
        for item in referrers:
            is_applicant = ""
            if item.is_applicant:
                is_applicant = _('yes')
            data.append( [Paragraph(to_v(item.name), styleN),
                          Paragraph(to_v(item.email), styleN),
                          Paragraph(to_v(item.phones), styleN),
                          Paragraph(to_v(is_applicant), styleN)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)


    styleF = copy.copy(styles['Normal'])
    styleF.alignment = TA_RIGHT
    styleF.fontSize = 9
    data = [[Paragraph("<br/><br/>%s<br/><br/>%s<br/>%s" % \
                       ("Santa fe, ..... de .......... de 20....",
                        '..................................................',
                        _('signature_applicant')), styleF)],]
    t = Table(data, colWidths='*')
    t.setStyle(TableStyle([('VALIGN',(-1,-1),(-1,-1),'BOTTOM'),
                           ('ALIGN',(0,0),(0,0),'RIGHT'),]))
    content.append(t)

    doc.build(content, onFirstPage=firstPage, onLaterPages=laterPages,canvasmaker=NumberedCanvas )
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
    styleH5 =  copy.copy(styles['Heading5'])
    styleN  =  copy.copy(styles['Normal'])
    styleN.fontSize = 8
    styleTable = TableStyle([('GRID', (0,1), (-1,-1), 1, colors.black),
                             ('FONTSIZE', (0, 0), (-1, -1), 8), 
                             ('BACKGROUND', (0, 1), (-1, 1), colors.Color(0.9,0.9,0.9)),
                             ('SPAN',(0,0),(0, 0)),])
    styleTableObs = TableStyle([('GRID', (0,1), (-1,-1), 1, colors.Color(0.9,0.9,0.9)),
                                ('FONTSIZE', (0, 0), (-1, -1), 8),])
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
    content.append(Paragraph( _('subscription_production_form') , styleH5))
    content.append(space)
    content.append(Paragraph(to_cv(_('proyect_name'), production.proyect.name), styleN))

    if production.proyect.description:
        content.append(space)
        data = [[_('description')],]
        data.append([[Paragraph(to_v(production.proyect.description), styleN)]])
        t = Table(data, colWidths='*')
        t.setStyle(styleTableObs)
        content.append(t)
    
    if production.observations:
        content.append(space)
        data = [[_('observations')],]
        data.append([[Paragraph(to_v(production.observations), styleN)]])
        t = Table(data, colWidths='*')
        t.setStyle(styleTableObs)
        content.append(t)

        
    if production.db_name or production.encoding or production.user_owner or production.user_access:
        data = [[_('database')]]
        content.append(space)
        data.append([_('name'),_('encoding'),_('user_owner'),_('user_access')])
        data.append([to_v(production.db_name),
                     to_v(production.encoding),
                     to_v(production.user_owner),
                     to_v(production.user_access),])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)


    if production.db_space_to_start or production.db_space_at_year or production.db_space_after or \
       production.fs_space_to_start or production.fs_space_at_year or production.fs_space_after:
        data = [[_('estimated_volume_data')],['',_('space_to_start'),_('space_at_year'),_('space_after')],]
        content.append(space)
        if production.db_space_to_start or production.db_space_at_year or production.db_space_after:
            data.append( [_('database'),
                          to_v(production.db_space_to_start),
                          to_v(production.db_space_at_year),
                          to_v(production.db_space_after)])
        if production.fs_space_to_start or production.fs_space_at_year or production.fs_space_after:
            data.append( [_('filesystem'),
                          to_v(production.fs_space_to_start),
                          to_v(production.fs_space_at_year),
                          to_v(production.fs_space_after)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)


    if production.minimum_memory or production.suggested_memory or \
       production.minimum_disk_space or production.suggested_disk_space or \
       production.minimum_processor or production.suggested_processor:
        data = [[_('hardware_requirements')],['',_('minimum'), _('recommended')],]
        content.append(space)
        if production.minimum_memory or production.suggested_memory:
            data.append( [_('memory'), to_v(production.minimum_memory),to_v(production.suggested_memory)])
        if production.minimum_disk_space or production.suggested_disk_space:
            data.append( [_('disk'), to_v(production.minimum_disk_space),to_v(production.suggested_disk_space)])
        if production.minimum_processor or production.suggested_processor:
            data.append( [_('processor'), to_v(production.minimum_processor), to_v(production.suggested_processor)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

            
    software = ProductionSoftwareRequirement.objects.filter(production_form=proyect_id)
    if software:
        data = [[_('software_requirements')],[_('name'), _('version')],]
        content.append(space)
        for item in software:
            data.append( [to_v(item.name),to_v(item.version)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)
        
    data = [[_('connection_sources')],[_('name'),_('ip_address'),_('service'),_('observations')],]
    sources = ProductionConnectionSource.objects.filter(production_form=proyect_id)
    if sources:
        content.append(space)
        for item in sources:
            data.append( [to_v(item.name), to_v(item.ip), to_v(item.service), to_v(item.observations)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    data = [[_('connection_targets')],[_('name'),_('ip_address'),_('service'),_('port'),_('ip_firewall')],]
    targets = ProductionConnectionTarget.objects.filter(production_form=proyect_id)
    if targets:
        content.append(space)
        for item in targets:
            data.append( [item.name,
                          to_v(item.ip),
                          to_v(item.service),
                          to_v(item.port),
                          to_v(item.ip_firewall)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    
    variables = MonitoredVariable.objects.filter(production_form=proyect_id)
    if variables:
        data = [[_('variables_to_be_monitored')],[_('variable'), _('periodicity'), _('preserving_history_by')],]
        content.append(space)
        for item in variables:
            data.append( [Paragraph(to_v(item.name), styleN),
                          Paragraph(to_v(item.periodicity), styleN),
                          Paragraph(to_v(item.preserving_history_by), styleN)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)

    hitos = Milestone.objects.filter(production_form=proyect_id)
    if hitos:
        data = [[_('milestones_during_the_year')],[_('milestone'), _('date'), _('duration_in_days')],]
        content.append(space)
        for item in hitos:
            data.append( [Paragraph(to_v(item.description), styleN),
                          Paragraph(to_v(item.duration), styleN),
                          Paragraph(to_v(str(item.date_event.strftime("%d/%m/%Y %H:%M"))), styleN)])
        t = Table(data, colWidths='*')
        t.setStyle(styleTable)
        content.append(t)


    styleF = copy.copy(styles['Normal'])
    styleF.alignment = TA_RIGHT
    styleF.fontSize = 9
    data = [[Paragraph("<br/><br/>%s, %s<br/><br/>%s<br/><br/>%s<br/>%s" % \
                       (_('full_name_applicant'),
                        "..................................................",
                        "Santa fe, ..... de .......... de 20....",
                        '..................................................',
                        _('signature_applicant')), styleF)],]
    t = Table(data, colWidths='*')
    t.setStyle(TableStyle([('VALIGN',(-1,-1),(-1,-1),'BOTTOM'),
                           ('ALIGN',(0,0),(0,0),'RIGHT'),]))
    content.append(t)

    doc.build(content, onFirstPage=firstPage, onLaterPages=laterPages, canvasmaker=NumberedCanvas)
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
    proyects = Proyect.production_pass_enabled()
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
        messages.warning(request, _('project_not_found'))
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
            msg = _('completed_application')
            context.update({'production_form_id': production.pk, 'msg': msg,
                            'link_to_application': reverse('print_production_form', args=[production.pk] ),
                            'link_to_new_application': reverse('production_step')})
            return render(request, 'outcome_success.html', context)
        else:
            transaction.savepoint_rollback( sid )
            
    except IntegrityError:
        logging.error('Integrity error for: %s' % proyect)
        transaction.savepoint_rollback( sid )

    msg = _('incomplete_application')
    context.update({'msg': msg})
    return render(request, 'outcome_error.html.html', context)
