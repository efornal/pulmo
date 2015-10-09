from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import logging
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils import translation

#from .forms import ApplicationFormForm


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

def new_step2(request):
    request.session['proyect']['name'] = request.POST['name']
    request.session['proyect']['description'] = request.POST['description']
    request.session['application']['db_name'] = request.POST['db_name']
    request.session['application']['encoding'] = request.POST['encoding']
    request.session['application']['user_owner'] = request.POST['user_owner']
    request.session['application']['user_access'] = request.POST['user_access']
    request.session['application']['observations'] = request.POST['observations']

    # FIXME LOG
    for s in request.session.items():
        logging.warning(s)

    return render(request, 'new_step2.html')

def new_step3(request):
    request.session['software']['names'] = request.POST.getlist('names[]')
    request.session['software']['versions'] = request.POST.getlist('versions[]')
    
    # FIXME LOG
    for s in request.session.items():
        logging.warning(s)

    return render(request, 'new_step3.html')

def new_step4(request):
    request.session['computers']['names'] = request.POST.getlist('names[]')
    request.session['computers']['ips'] = request.POST.getlist('ips[]')
    request.session['computers']['observations'] = request.POST.getlist('observations[]')

    # FIXME LOG
    for s in request.session.items():
        logging.warning(s)

    return render(request, 'new_step4.html')

def new_step5(request):
    request.session['scv']['usernames'] = request.POST.getlist('usernames[]')
    request.session['scv']['permisions'] = request.POST.getlist('permisions[]')

    # FIXME LOG
    for s in request.session.items():
        logging.warning(s)

    return render(request, 'new_step5.html')


def save(request):
    request.session['referrer']['names'] = request.POST.getlist('names[]')
    request.session['referrer']['emails'] = request.POST.getlist('emails[]')
    request.session['referrer']['phones'] = request.POST.getlist('phones[]')
    request.session['referrer']['applicants'] = request.POST.getlist('applicants[]')
    # FIXME LOG
    for s in request.session.items():
        logging.warning(s)
    logging.warning(request.POST)



    
    request.session['has_registered'] = True    
    return HttpResponse("Values: "  )
