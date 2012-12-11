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
    'timegraph',
    'south',
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
