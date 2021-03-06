from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4#^9%)zfhtz$jz1rn3!=+!txo9c0)km43i*ovuhmtbg!c6@h5c'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar',
]

# MIDDLEWARE = MIDDLEWARE + [
#     'debug_toolbar.middleware.DebugToolbarMiddleware'
# ]

INTERNAL_IPS = ['127.0.0.1', '127.17.0.1', '127.0.0.1:8000']

try:
    from .local import *
except ImportError:
    pass
