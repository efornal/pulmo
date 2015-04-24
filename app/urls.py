from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('app.views',
    url('^save','save', name='save'),
    url('^new','new', name='new'),
    url(r'^$', 'index', name='index'),
)


