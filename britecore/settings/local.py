from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w8pq#t#$a8(rzv+lyrix55@6slp7u1n0fopt9=2um&@*+65$=$'

DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'POST': 5432,
        'NAME': 'brite',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
    }
}


STATIC_URL = '/static/'

# CORS_ORIGIN_WHITELIST = ('*')
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

