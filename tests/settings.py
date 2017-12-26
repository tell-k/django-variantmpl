import os
from django import VERSION

here = os.path.dirname(__file__)

DEBUG = False

if VERSION < (1, 10):
    TEMPLATE_DEBUG = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(here, 'tests', 'templates')],
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


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',

    'tests',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
SECRET_KEY = 'secret_key_for_testing'
MIDDLEWARE_CLASSES = []

PASSWORD_HASHERS = (
   'django.contrib.auth.hashers.MD5PasswordHasher',
)
