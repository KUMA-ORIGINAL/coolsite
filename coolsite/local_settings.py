from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-_ac@mh%xtve)0z$lfg(ug!n0%5+aqb()g)(*#q&re2*vyj90t6'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_DIR = BASE_DIR / 'static'
STATICFILES_DIRS = [STATIC_DIR]