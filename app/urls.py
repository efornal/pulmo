from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('app.views',
    url(r'^$', 'index', name='index'),
    url('^save','save', name='save'),
    url(r'^new/step/1', 'new_step1', name='new_step1'),
    url(r'^new/step/2', 'new_step2', name='new_step2'),
    url(r'^new/step/3', 'new_step3', name='new_step3'),
    url(r'^new/step/4', 'new_step4', name='new_step4'),
    url(r'^new/step/5', 'new_step5', name='new_step5'),
)


