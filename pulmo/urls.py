from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

admin.autodiscover()

urlpatterns  = i18n_patterns(
    url(r'^', include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
