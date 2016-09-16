from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^save',views.save, name='save'),
    url(r'^new/1/application', views.new_step1, name='new_step1'),
    url(r'^new/2/application', views.new_step2, name='new_step2'),
    url(r'^new/3/application', views.new_step3, name='new_step3'),
    url(r'^new/4/application', views.new_step4, name='new_step4'),
    url(r'^new/5/application', views.new_step5, name='new_step5'),
    url(r'^print_application_form/(\d+)/$', views.print_application_form, name='print_application_form'),
    url(r'^new/production', views.production_step, name='production_step'),
    url(r'^new/1/production', views.production_step1, name='production_step1'),
    url(r'^new/2/production', views.production_step2, name='production_step2'),
    url(r'^new/3/production', views.production_step3, name='production_step3'),
    url(r'^new/4/production', views.production_step4, name='production_step4'),
    url(r'^new/5/production', views.production_step5, name='production_step5'),
    url(r'^new/6/production', views.production_step6, name='production_step6'),
    url(r'^print_production_form/(\d+)/$', views.print_production_form, name='print_production_form'),
]


