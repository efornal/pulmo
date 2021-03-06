# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

from django.shortcuts import redirect

def redirect_without_post(view):
    def wrap(request, *args, **kwargs):
        if request.method != 'POST':
            return redirect('index')
        else:
            return view(request, *args, **kwargs)
    return wrap

def redirect_without_production_post(view):
    def wrap(request, *args, **kwargs):
        if request.method != 'POST':
            return redirect('production_step')
        else:
            return view(request, *args, **kwargs)
    return wrap

def redirect_if_has_registered(view):
    def wrap(request, *args, **kwargs):
        if 'has_registered' in request.session and request.session['has_registered']:
            request.session['has_registered'] = False
            return redirect('index')
        else:
            return view(request, *args, **kwargs)
    return wrap

def redirect_if_has_production_registered(view):
    def wrap(request, *args, **kwargs):
        if 'has_registered' in request.session and request.session['has_registered']:
            request.session['has_registered'] = False
            return redirect('production_step')
        else:
            return view(request, *args, **kwargs)
    return wrap


def allow_view_users_requests(view):
    def wrap(request, *args, **kwargs):
        if hasattr(settings, 'ALLOW_VIEW_USERS_REQUESTS') and \
           settings.ALLOW_VIEW_USERS_REQUESTS:
            return view(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrap
