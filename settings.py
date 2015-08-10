# Django settings for django-timegraph project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'timegraph.sqlite',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'timegraph',
)

TIMEGRAPH_CACHE_PREFIX = 'timegraph'
TIMEGRAPH_RRD_ROOT = '/var/lib/rrdcached/db'
USE_TZ = True
