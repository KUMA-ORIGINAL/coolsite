from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'kumafsdfsfsddjango-insecure-_ac@mh%xtve)0z$lfg(ug!n0%5+aqb()g)(*#q&re2*vyj90t6'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'coolsite',
        'USER': 'user_coolsite',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

STATIC_ROOT = BASE_DIR / 'static'
STATIC_DIR = BASE_DIR / 'static'
STATICFILES = [STATIC_DIR]
