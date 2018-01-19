# Django settings for i5k project.
from os import path
import sys
from sys import platform
import os
import socket
# to fix axe issue on Windows, see: https://github.com/jazzband/django-axes/issues/204
if platform == 'win32':
    from win_inet_pton import inet_pton
from kombu import Exchange, Queue  # For celery

PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))

DEBUG = True

TEST_RUNNER = 'i5k.testing.MyDiscoverRunner'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(PROJECT_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'app.context_processors.is_login_enabled',
                'app.context_processors.is_analytics_enabled',
            ],
        },
    },
]

ALLOWED_HOSTS = (
    '*',
)

ADMINS = (
     ('Your Name', 'Your@email.address'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django-bioinfo',
        'USER': 'django-bioinfo',
        'PASSWORD': 'django1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = path.join(PROJECT_ROOT, 'media').replace('\\','/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = path.join(PROJECT_ROOT, 'static').replace('\\','/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'pipeline.finders.PipelineFinder',
    'pipeline.finders.CachedFileFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'n(bd1f1c%e8=_xad02x5qtfn%wg2pi492e$8_erx+d)!tpeoim'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'app.middleware.SocialAuthExceptionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'i5k.urls'

WSGI_APPLICATION = 'i5k.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'axes',
    'rest_framework',
    'rest_framework_swagger',
    'pipeline',
    'app',
    'blast',
    'suit',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'hmmer',
    'clustal',
)

FILEBROWSER_SUIT_TEMPLATE = True
FILEBROWSER_DIRECTORY = ''
FILEBROWSER_VERSIONS_BASEDIR = '_versions/'
FILEBROWSER_MAX_UPLOAD_SIZE = 10737418240 # 10GB
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv', '.docx'],
    'FASTA': ['.fa', '.faa', '.fna', '.fsa', '.ffn', '.mpfa', '.faa', '.fasta', '.cds', '.pep', '.seq'],
    'FASTQ': ['.fq', '.fastq'],
    'SAM': ['.sam', '.bam'],
    'WIG': ['.wig', '.bw', '.bigwig'],
    'JSON': ['.json'],
    'GFF': ['.gff', '.gff3']
}
FILEBROWSER_SELECT_FORMATS = {
    'file': ['Folder', 'Image', 'Document', 'Video', 'Audio', 'FASTA', 'FASTQ', 'SAM', 'WIG', 'JSON', 'GFF'],
    'document': ['Document'],
    'FASTA': ['FASTA'],
    'FASTQ': ['FASTQ'],
    'SAM': ['SAM'],
    'WIG': ['WIG'],
    'JSON': ['JSON'],
    'GFF': ['GFF'],
}
FILEBROWSER_VERSIONS = {
    'admin_thumbnail': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop'},
    'thumbnail': {'verbose_name': 'Thumbnail (1 col)', 'width': 60, 'height': 60, 'opts': 'crop'},
    'small': {'verbose_name': 'Small (2 col)', 'width': 140, 'height': '', 'opts': ''},
    'medium': {'verbose_name': 'Medium (4col )', 'width': 300, 'height': '', 'opts': ''},
    'big': {'verbose_name': 'Big (6 col)', 'width': 460, 'height': '', 'opts': ''},
    'large': {'verbose_name': 'Large (8 col)', 'width': 680, 'height': '', 'opts': ''},
}

# Django Suit configuration
SUIT_CONFIG = {
    'ADMIN_NAME': 'i5k Admin',
    'MENU_OPEN_FIRST_CHILD': False,
    'MENU_EXCLUDE': (),
    'MENU': (
        {'app': 'blast', 'label': 'BLAST', 'icon':'icon-leaf', 'models': (
            {'model': 'blastqueryrecord'},
            {'model': 'organism'},
            {'model': 'sequencetype'},
            {'model': 'blastdb'},
            {'model': 'jbrowsesetting'},
            {'model': 'sequence'},
        )},
        {'app': 'hmmer', 'label': 'Hmmer', 'icon':'icon-leaf', 'models': (
            {'model': 'hmmerdb'},
            {'model': 'hmmerqueryrecord'},
        )},
        {'app': 'clustal', 'label': 'clustal', 'icon':'icon-leaf', 'models': (
            {'model': 'clustalqueryrecord'},
        )},
        # auth and axes
        {'label': 'Auth', 'icon':'icon-lock', 'models': (
            {'model': 'auth.user'},
            {'model': 'auth.group'},
            {'model': 'axes.accessattempt'},
            {'model': 'axes.accesslog'},
        )},
        {'label': 'File Browser', 'icon':'icon-hdd', 'url': 'fb_browse'},
    ),
}

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
# Query maximum limit
BLAST_QUERY_MAX = 10
HMMER_QUERY_MAX = 10

# Query maximum size (k bytes)
BLAST_QUERY_SIZE_MAX = 1000

# Celery Settings
CELERY_DEFAULT_QUEUE = 'i5k'
CELERY_DEFAULT_EXCHANGE = 'i5k'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_ROUTING_KEY = 'i5k'
CELERY_QUEUES = (
    Queue('i5k', Exchange('i5k'), routing_key='i5k'),
)
BROKER_URL = 'amqp://'
CELERY_RESULT_BACKEND = 'amqp://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = TIME_ZONE
CELERY_DISABLE_RATE_LIMITS = True
# CELERY_ENABLE_UTC = True

USE_CACHE = False
# memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': None, # never expire
    }
}

# django-axes
AXES_LOGIN_FAILURE_LIMIT = 3
AXES_LOCK_OUT_AT_FAILURE = True
AXES_USE_USER_AGENT = True
AXES_COOLOFF_TIME = 1 # 1 hour
AXES_LOGGER = 'axes.watch_login'
AXES_LOCKOUT_TEMPLATE = 'app/login_lockout.html'
AXES_LOCKOUT_URL = None
AXES_VERBOSE = True

# django-pipeline
if not DEBUG:
    STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
# django-pipeline 1.6
PIPELINE = {
    'STYLESHEETS':{
        'app-layout': {
            'source_filenames': (
                'app/content/site.css',
                'app/content/bootstrap.min.css',
            ),
            'output_filename': 'app/content/app-layout.min.css',
        },
        'blast-results': {
            'source_filenames': (
                'blast/css/codemirror.css',
                'blast/css/xq-light.css',
                'blast/css/kendo.common-bootstrap.core.css',
                'blast/css/kendo.bootstrap.min.css',
                'blast/css/jquery-ui.min.css',
                'blast/dataTables/css/jquery.dataTables.min.css',
                'blast/dataTables/css/dataTables.scroller.min.css',
                'blast/dataTables/css/dataTables.colReorder.min.css',
                'blast/dataTables/css/dataTables.bootstrap.css',
                'blast/css/bootstrap-select.min.css',
                'blast/css/bootstrap-switch.min.css',
                'blast/css/blast-results.css',
            ),
            'output_filename': 'blast/css/blast-results.min.css',
        },
        'blast-css': {
            'source_filenames': (
                'blast/css/main.css',
            ),
            'output_filename': 'blast/css/blast-css.min.css',
        },
        'clustal-css': {
            'source_filenames': (
                'clustal/css/main.css',
            ),
            'output_filename': 'clustal/css/clustal-css.min.css',
        },
        'hmmer-css' : {
            'source_filenames': (
                'hmmer/css/main.css',
            ),
            'output_filename': 'hmmer/css/hmmer-css.min.css',
        },
    },
    'JAVASCRIPT': {
        'app-layout': {
            'source_filenames': (
                'app/scripts/jquery-1.11.1.min.js',
                'app/scripts/bootstrap.min.js',
                'app/scripts/respond.min.js',
            ),
            'output_filename': 'app/scripts/app-layout.min.js',
        },
        'blast-results': {
            'source_filenames': (
                'blast/scripts/chroma.min.js',
                'blast/scripts/codemirror-compressed.js',
                'blast/scripts/kendo-hotdogee.js',
                'blast/scripts/jquery-ui.min.js',
                'blast/scripts/dragscrollable.js',
                'blast/dataTables/js/jquery.dataTables-hotdogee.js',
                'blast/dataTables/js/dataTables.scroller.js',
                'blast/dataTables/js/dataTables.colReorder.min.js',
                'blast/dataTables/js/dataTables.tableTools.min.js',
                'blast/dataTables/js/dataTables.bootstrap.js',
                'blast/scripts/underscore-min.js',
                'blast/scripts/backbone-min.js',
                'blast/scripts/scribl.1.1.5-hotdogee.js',
                'blast/scripts/bootstrap-select-hotdogee.js',
                'blast/scripts/bootstrap-switch.min.js',
                'blast/scripts/blast-results.js',
            ),
            'output_filename': 'blast/scripts/blast-results.min.js',
        },
        'blast-js': {
            'source_filenames': (
                'blast/scripts/underscore-min.js',
                'blast/scripts/jquery.hoverIntent.minified.js',
                'blast/scripts/jquery.validate.min.js',
                'blast/scripts/blast-multi.js',
            ),
            'output_filename': 'blast/scripts/blast-js.min.js',
        },
        'clustal-js': {
            'source_filenames': (
                'clustal/scripts/underscore-min.js',
                'clustal/scripts/jquery.hoverIntent.minified.js',
                'clustal/scripts/jquery.validate.min.js',
                'clustal/scripts/clustal-multi.js',
            ),
            'output_filename': 'clustal/scripts/clustal-js.min.js',
        },
        'hmmer-js': {
            'source_filenames': (
                'hmmer/scripts/underscore-min.js',
                'hmmer/scripts/jquery.hoverIntent.minified.js',
                'hmmer/scripts/jquery.validate.min.js',
                'hmmer/scripts/hmmer-multi.js',
            ),
            'output_filename': 'hmmer/scripts/hmmer-js.min.js',
        },
        'sso-js': {
            'source_filenames': (
                'webapollo_sso/scripts/underscore-min.js',
                'webapollo_sso/scripts/sso-datatable.js',
            ),
            'output_filename': 'sso/scripts/sso-js.min.js',
        },
    },
}

if not DEBUG:
    PIPELINE['PIPELINE_ENABLED'] = True
    PIPELINE['CSSMIN_BINARY'] = 'cssmin'
    PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.cssmin.CSSMinCompressor'
    PIPELINE['JS_COMPRESSOR']  = 'pipeline.compressors.jsmin.JSMinCompressors'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

# Email backend
EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'webmaster@localhost'

try:
    HOSTNAME = socket.gethostname()
except:
    HOSTNAME = 'localhost'

LOGIN_ENABLED = False
ANALYTICS_ENABLED = False

# Use settings for production
USE_PROD_SETTINGS = False
if USE_PROD_SETTINGS:
    from settings_prod import *

sys.path.append('%s/misc' % path.dirname(path.abspath(path.dirname(__file__))))
