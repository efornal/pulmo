# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

admin.autodiscover()

urlpatterns  = i18n_patterns(
    url(r'^', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
