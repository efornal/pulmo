from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('app.views',
    url(r'^$', 'index', name='index'),
    url('^save','save', name='save'),
    url(r'^new/1/application', 'new_step1', name='new_step1'),
    url(r'^new/2/application', 'new_step2', name='new_step2'),
    url(r'^new/3/application', 'new_step3', name='new_step3'),
    url(r'^new/4/application', 'new_step4', name='new_step4'),
    url(r'^new/5/application', 'new_step5', name='new_step5'),
    url(r'^print_application_form/(\d+)/$', 'print_application_form', name='print_application_form'),
    url(r'^new/production', 'production_step', name='production_step'),
    url(r'^new/1/production', 'production_step1', name='production_step1'),
    url(r'^new/2/production', 'production_step2', name='production_step2'),
    url(r'^new/3/production', 'production_step3', name='production_step3'),
    url(r'^new/4/production', 'production_step4', name='production_step4'),
    url(r'^new/5/production', 'production_step5', name='production_step5'),
    url(r'^new/6/production', 'production_step6', name='production_step6'),
    url(r'^print_production_form/(\d+)/$', 'print_production_form', name='print_production_form'),
)


