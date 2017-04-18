# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from app import views
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGIN_REDIRECT_URL},
        name='logout'),
    url(r'^$', views.index, name='index'),
    url('^save',views.save, name='save'),
    url('^check_server',views.check_server, name='check_server'),
    url(r'^new/application', views.new_step1, name='new_step1'),
    url(r'^new/2/application', views.new_step2, name='new_step2'),
    url(r'^new/3/application', views.new_step3, name='new_step3'),
    url(r'^new/4/application', views.new_step4, name='new_step4'),
    url(r'^new/5/application', views.new_step5, name='new_step5'),
    url(r'^new/production', views.production_step, name='production_step'),
    url(r'^new/1/production', views.production_step1, name='production_step1'),
    url(r'^new/2/production', views.production_step2, name='production_step2'),
    url(r'^new/3/production', views.production_step3, name='production_step3'),
    url(r'^new/4/production', views.production_step4, name='production_step4'),
    url(r'^new/5/production', views.production_step5, name='production_step5'),
    url(r'^new/6/production', views.production_step6, name='production_step6'),
]


