from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'murex.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#    url('^', include('django.contrib.auth.urls')),

    url(r'^app/', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
