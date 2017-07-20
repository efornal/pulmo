# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Django settings for pulmo project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ldap

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = 'https://servicios.unl.edu.ar/pulmo'
APPLICATION_NAME = "Pulmo"
APPLICATION_DESC = "Project requests"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@(p@8_b$kl37vsh_p8urf@^681q&qpz+b+f3-o(aj4cjnv*_81'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# ADMINS = (
#     ('name', 'email'),
# )

# MANAGERS = (
#     ('name', 'email'),
# )
# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jquery',
    'jquery_ui',
    'bootstrap_ui',
    'django_extensions',
    'bootstrap_themes',
    'app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'app.middleware.ForceLangMiddleware',
)

ROOT_URLCONF = 'pulmo.urls'

import os
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pulmo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pulmo_db',
        'USER': 'pulmo_owner',
        'PASSWORD': 'owner',
        'PORT': '5432',
        'HOST': 'localhost',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es'

LANGUAGES = (
  ('es', _('Spanish')),
  ('en', _('English')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL='/static/'

LOGIN_URL='/login/'
LOGIN_REDIRECT_URL = '/'

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

LOCALE_PATHS = (
     BASE_DIR + '/locale', )


LOGS_VISUALIZATION_CHOICES = (
    ('1', 'Log-Analizer'),
    ('2', 'Archivo en Log-Server'),
)

# =================================\
# ganeti configuration
GANETI_INSTANCES_URL = 'https://cluster:5080/2/instances'
# =================================/


# =================================\
# redmine configuration
#
# Si REDMINE_ENABLE_TICKET_CREATION está habilitado:
# Para formulario de aplicación
#  - crea ticket principal con solicitud de aplicación -servidor de test-
#  - crea subtarea con solicitud de usuarios ssh (+ssh_users)
#  - crea subtarea con usuarios extras de base de datos (+extra_database_users)
#  - crea subtarea para monitoreo en test
#  - crea subtarea configuración de nivel de logs en test
#  - crea subtarea para solicitud de máquina virtual de integración (+requires_integration)
# Para formulario de producción
#  - crea ticket principal con solicitud de aplicación -servidor de producción-
#  - crea subtarea para monitoreo en producción
#  - crea subtarea configuración de nivel de logs en producción
#  - crea subtarea configuración de backup en producción
#
#    + indica se debió especificar el dato en formulario para que se realice el ticket. 
REDMINE_ENABLE_TICKET_CREATION = False
#
REDMINE_URL='http://redmine_url'
REDMINE_USERNAME="username"
REDMINE_PASSWORD = "password"
REDMINE_PROJECT = "proyect_name"
REDMINE_TRACKER_ID = None
REDMINE_STATUS_ID = None
REDMINE_PRIORITY_ID = None
REDMINE_ASSIGNED_TO_ID = None
# maximum limit users found as observers of a ticket.
# If there are more than this value, the addition of the ticket is omitted obervadores
REDMINE_MAXIMUM_OBSERVER_FOUND = 5
#
#
# Url where the procedure to resolve the ticket will be explained
#REDMINE_SSH_USERS_URL   = "https://host/doc"
#REDMINE_MONITORING_URL  = "https://host/doc"
#REDMINE_LOG_LEVEL_URL   = "https://host/doc"
#REDMINE_BACKUP_URL      = "https://host/doc"
#REDMINE_INTEGRATION_URL = "https://host/doc"
#
# =================================/


# =================================\
# zabbix configuration
ZABBIX_API_URL = 'http://url_to_zabbix/'
ZABBIX_API_USERNAME = ''
ZABBIX_API_PASSWORD = ''
ZABBIX_API_MONITORING_TEMPLATE_ID = None
ZABBIX_API_PGSQL_TEMPLATE_ID = None
ZABBIX_API_MYSQL_TEMPLATE_ID = None

# when's defined, look for the host with, and without, the suffix (ex.: .com)
ZABBIX_API_HOST_SUFIX = '' 

# =================================/


# =================================\
# ldap configuration

LDAP_SERVER = 'ldap://host_ldap:port'

LDAP_DN = 'dc=domain,dc=edu,dc=ar'

# Organizational Unit for Person
LDAP_PEOPLE = 'People'
LDAP_GROUP  = 'Group' # ou=Entry
# =================================/

# django configuration
SUIT_CONFIG = {
    'ADMIN_NAME': APPLICATION_NAME
}

# =================================\
# django ldap configuration
#
#
# Ldap Group Type
from django_auth_ldap.config import LDAPSearch, PosixGroupType
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou={},{}".format(LDAP_GROUP,LDAP_DN),
                                    ldap.SCOPE_SUBTREE, "(objectClass=posixGroup)"
)
AUTH_LDAP_GROUP_TYPE =  PosixGroupType()
#
#
# User will be updated with LDAP every time the user logs in.
# Otherwise, the User will only be populated when it is automatically created.
AUTH_LDAP_ALWAYS_UPDATE_USER = True
#
#
# Simple group restrictions
# AUTH_LDAP_REQUIRE_GROUP = "cn=users,ou={},{}".format(LDAP_GROUP,LDAP_DN)
# AUTH_LDAP_DENY_GROUP = "cn=denygroup,ou={},{}".format(LDAP_GROUP,LDAP_DN)
#
# Defines the django admin attribute
# according to whether the user is a member or not in the specified group
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=users,ou={},{}".format(LDAP_GROUP,LDAP_DN),
    "is_staff": "cn=users,ou={},{}".format(LDAP_GROUP,LDAP_DN),
    "is_superuser": "cn=admin,ou={},{}".format(LDAP_GROUP,LDAP_DN),
}
#
# Ldap User Auth
#AUTH_LDAP_BIND_DN = "cn={},{}".format(LDAP_USERNAME,LDAP_DN)
#AUTH_LDAP_BIND_PASSWORD = LDAP_PASSWORD

AUTH_LDAP_SERVER_URI = LDAP_SERVER

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou={},{}".format(LDAP_PEOPLE,LDAP_DN),
                                   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
#    'django.contrib.auth.backends.ModelBackend',
)

# =================================/


# #loggin querys in develompent
# if DEBUG:
#     import logging
#     l = logging.getLogger('django.db.backends')
#     l.setLevel(logging.DEBUG)
#     l.addHandler(logging.StreamHandler())
#     logging.basicConfig(
#         level = logging.DEBUG,
#         format = " %(levelname)s %(name)s: %(message)s",
#     )

# # Enable debug for ldap server connection
# logger = logging.getLogger('django_auth_ldap')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


# import logging
# logger = logging.getLogger('django_auth_ldap')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


# import warnings
# warnings.filterwarnings(
#         'error', r"DateTimeField .* received a naive datetime",
#         RuntimeWarning, r'django\.db\.models\.fields')
