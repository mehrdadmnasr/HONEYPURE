"""
Django settings for HoneyPure project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages
# for set in liara database
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^cjwd@wl*8&57ku#bc@^#$hrx0zr)4l1tp)d(rs7mo%879_s%0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# movaghat rooye system khodam meghdar nadarad
ALLOWED_HOSTS = ['honeypure.liara.run', 'localhost']
#ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'

# Application definition

INSTALLED_APPS = [
    'products.apps.ProductsConfig',
    'pages.apps.PagesConfig',
    'blog.apps.BlogConfig',
    'accounts.apps.AccountsConfig',
    'cart.apps.CartConfig',
    'translation.apps.TranslationConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'django.contrib.humanize',
    'django.contrib.sites',

    # برنامه‌های django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Providers
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # اضافه کردن AccountMiddleware
]

ROOT_URLCONF = 'HoneyPure.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pages.context_processors.cart_total_items',
            ],
        },
    },
]

WSGI_APPLICATION = 'HoneyPure.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'honey_db',
#        'USER': 'postgres',
#        'PASSWORD' : '1682168',
#        'HOST' : 'localhost',
#    }

    # for set in liara database
    'default': dj_database_url.config(
        default='postgres://root:OeVq9MnPn9aQhRp42Ey37uD7@honeypure-db:5432/honeypure-db'
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('fa', 'Persian'),
    ('fr', 'French'),
    ('tr', 'Turkish'),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

EXCLUDE_PATHS = [
    os.path.join(BASE_DIR, 'env'),
    os.path.join(BASE_DIR, 'AppData'),  # مسیرهای مشکل‌دار
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'HoneyPure/static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Media settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#messages
MESSAGE_TAGS = {
    messages.ERROR: "danger",
}

SITE_ID = 2

# email sendeing
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mehrdad.m.nasr@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

PAYPAL_CLIENT_ID = 'your-client-id'
PAYPAL_CLIENT_SECRET = 'your-client-secret'
