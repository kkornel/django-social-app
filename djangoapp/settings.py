"""
Django settings for djangoapp project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY for development:
# SECRET_KEY = '#r5ac@-nk0tn!x0+liwgg4(tpel)vplw3q^rfdaht&_xrg_9nz'

# SECRET_KEY for production:
# If we want to generate new key:
# (cmd) > python
# >>> import secrets
# >>> secrets.token_hex(24)
# >>> NEW_KEY
SECRET_KEY = os.environ.get('DJANGO_SOCIAL_APP_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = (os.environ.get('DEBUG_VARIABLE') == 'True')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mydjangosocialapp.herokuapp.com']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'crispy_forms',
    'bootstrap_modal_forms',
    'widget_tweaks',
    'storages',
    # Local
    'users.apps.UsersConfig',
    'social.apps.SocialConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoapp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# SQLite 3
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mt_django_app',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format':
            '[%(levelname)s] [%(asctime)s] [%(name)s.%(funcName)s] ->  %(message)s',
            # 'format': '[%(levelname)s: %(asctime)s] -> %(name)s.%(funcName)s() ->  %(message)s',
            # 'format': '[ %(levelname)-8s] -> %(name)s.%(funcName)s ->  %(message)s',
            'datefmt': '%H:%M:%S',
            # 'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        # 'file': {
        #     'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        # }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'formatter': 'file',
        #     'filename': 'debug.log'
        # }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console']
            # 'handlers': ['console', 'file']
        }
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# I've created custom User in users.models, because I wanted to
# authenticate users using email address instead of a username.
AUTH_USER_MODEL = 'users.User'

# Telling crispy to use bootstrap v.4 as default
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Tells Django where to go after successful login.
# If not specified Django looks for /profile/.
LOGIN_REDIRECT_URL = 'home'

# Tells Django where to go if someone tries to go for a login required view,
# but he is not logged in. If not specified Django looks for /profile/login.
LOGIN_URL = 'login'

LOGOUT_REDIRECT_URL = 'login'

# Path where we want to store uploaded files (locally).
# For a performance reasons, they are stored on the file system, not in database.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Public URL of MEDIA_ROOT directory.
# This is how we will access media through the browser.
MEDIA_URL = '/media/'

# Email configuration for password-reset.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
EMAIL_FROM_EMAIL = 'django@noreply.com'

# Keys for RECAPTCHA.
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')

# REST
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
}

# AWS S3
AWS_ACCESS_KEY_ID = os.environ.get('AWS_DJANGO_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_DJANGO_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_DJANGO_STORAGE_BUCKET_NAME')

AWS_3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

django_heroku.settings(locals())
