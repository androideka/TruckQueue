"""
Django settings for Truck Queue project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import smtplib
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '11idlpdkm%d@(==@!nu+v+mm^632cwnvjh6=grvn&)e!ft3d-5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registration.backends.simple',
    'future',
    'django_twilio',
    'truck_queue',
]

ACCOUNT_ACTIVATION_DAYS = 7

REGISTRATION_AUTO_LOGIN = False

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'WebApp.urls'

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

WSGI_APPLICATION = 'WebApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases


from os.path import dirname, join
PROJECT_DIR = dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(PROJECT_DIR, 'db.sqlite3'),
    }
}

# Twilio account information
TWILIO_ACCOUNT_SID = 'AC6dd06745bc549844a50812e5e6704641'
TWILIO_AUTH_TOKEN = '2db43dd1e82eb4c19c82b12e6df891c3'


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

SITE_ID = 2

#DEFAULT_FROM_EMAIL = 'info@truckqueue.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
SERVER = smtplib.SMTP()
SERVER.connect(EMAIL_HOST, EMAIL_PORT)
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'truckqueue@gmail.com'
EMAIL_HOST_PASSWORD = 'gotruckyourself'

SERVER.starttls()
SERVER.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)