DEBUG = True

USE_CACHE = True

with open('/path/to/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

ALLOWED_HOSTS = (
    '.example.com',
)

MEDIA_URL = '/webapp/media/'
STATIC_URL = '/webapp/static/'
LOGIN_URL = '/webapp/login'
LOGIN_REDIRECT_URL = '/webapp/home'

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '127.0.0.1',
    'PORT': '5432',
    }
}

# Email backend
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'name@yourhost.com'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

#
# Use default 'django' logger to a file in /var/log/django/django.log
# and new log 'i5k' to /var/log/i5k/i5k.log
# See logging.md doc for more details.
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'normal': {
            'format': '%(name)s %(levelname)s %(asctime)s %(process)d [%(message)s] (file: %(pathname)s line: %(lineno)d)'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
       'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': os.getenv('ADMIN_LOG_LEVEL', 'ERROR'),
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'normal'
        },
        'django_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/django/django.log',
            'when': 'midnight',
            'backupCount': 60,
            'formatter': 'normal'
        },
        'i5k_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/django/i5k.log',
            'when': 'midnight',
            'backupCount': 60,
            'formatter': 'normal'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'normal'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins', 'django_file', 'console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
        'i5k': {
            'handlers': ['mail_admins', 'i5k_file', 'console'],
            'level': os.getenv('I5K_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    }
}

LOGIN_ENABLED = False
