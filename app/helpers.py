# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

def are_all_empty_params( params ):
    for key,value in params.iteritems():
        if value:
            return False
    return True

def to_v( field_value ):
    return field_value or ''

def to_absolute_url( relative_url='' ):
    return "%s%s" % (settings.BASE_URL,relative_url)
