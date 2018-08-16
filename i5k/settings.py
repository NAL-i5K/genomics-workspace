# Django settings for i5k project.
from os import path
import sys
import os
import socket

BASE_DIR = path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = path.dirname(os.path.abspath(__file__))

DEBUG = True

TEST_RUNNER = 'i5k.testing.MyDiscoverRunner'

# template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(BASE_DIR, 'i5k', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'django1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/home'

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
MEDIA_ROOT = path.join(BASE_DIR, 'media').replace('\\','/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = path.join(BASE_DIR, 'static').replace('\\','/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

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
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'i5k.urls'

# Python dotted path to the WSGI application used by Django's runserver.
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
    'pipeline',
    'app',
    'blast',
    'suit',  # suit must before admin
    'filebrowser',
    # Enable the admin:
    'django.contrib.admin',
    # Enable admin documentation:
    'django.contrib.admindocs',
    'proxy',
    'hmmer',
    'clustal',
)


# filebrowser settings
FILEBROWSER_DEBUG = False
FILEBROWSER_SUIT_TEMPLATE = True
FILEBROWSER_DIRECTORY = ''
FILEBROWSER_VERSIONS_BASEDIR = '_versions/'
FILEBROWSER_MAX_UPLOAD_SIZE = 10737418240 # 10GB
FILEBROWSER_EXTENSIONS = {
    'folder': [''],
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

# suit settings
ENABLE_JBROWSE_INTEGRATION = False

if ENABLE_JBROWSE_INTEGRATION:
    blast_models = (
            {'model': 'blastqueryrecord'},
            {'model': 'sequencetype'},
            {'model': 'blastdb'},
            {'model': 'jbrowsesetting'},  # only exsit when ENABLE_JBROWSE_INTEGRATION == True
            {'model': 'sequence'},
    )
else:
    blast_models = (
            {'model': 'blastqueryrecord'},
            {'model': 'sequencetype'},
            {'model': 'blastdb'},
            {'model': 'sequence'},
    )
suit_menu = (
    {'app': 'app', 'label': 'Organism', 'icon': 'icon-leaf', 'url': '/admin/app/organism/', 'models': (
        {'model': 'Organism'},
    )},
    {'app': 'blast', 'label': 'BLAST', 'icon': 'icon-leaf', 'models': blast_models},
    {'app': 'hmmer', 'label': 'Hmmer', 'icon': 'icon-leaf', 'models': (
        {'model': 'hmmerdb'},
        {'model': 'hmmerqueryrecord'},
    )},
    {'app': 'clustal', 'label': 'clustal', 'icon': 'icon-leaf', 'models': (
        {'model': 'clustalqueryrecord'},
    )},
    # auth and axes
    {'label': 'Auth', 'icon': 'icon-lock', 'url': '/admin/auth/user/', 'models': (
        {'model': 'auth.user'},
        {'model': 'auth.group'},
        {'model': 'axes.accessattempt'},
        {'model': 'axes.accesslog'},
    )},
    {'label': 'File Browser', 'icon': 'icon-hdd', 'url': 'fb_browse'},
)

# Django Suit configuration
SUIT_CONFIG = {
    'ADMIN_NAME': 'i5k Admin',
    'MENU_OPEN_FIRST_CHILD': False,
    'MENU_EXCLUDE': (),
    'MENU': suit_menu,
}

# Query maximum limit
BLAST_QUERY_MAX = 10
HMMER_QUERY_MAX = 10

# Query maximum size (k bytes)
BLAST_QUERY_SIZE_MAX = 1000

# Celery Settings
from kombu import Exchange, Queue
CELERY_TASK_DEFAULT_QUEUE = 'i5k'
CELERY_TASK_DEFAULT_EXCHANGE = 'i5k'
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'i5k'
CELERY_TASK_QUEUES = (
    Queue('i5k', Exchange('i5k'), routing_key='i5k'),
)
CELERY_BROKER_URL = 'amqp://'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = TIME_ZONE
CELERY_WORKER_DISABLE_RATE_LIMITS = True
CELERY_RESULT_BACKEND = 'rpc://'

# Use virtual environment or not
USE_VIRTUALENV = False
VIRTUALENV_ROOT = 'virtualenv/py2.7'

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

# django-restframework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

# django-pipeline
PIPELINE = {
    'STYLESHEETS': {
        'app-layout': {
            'source_filenames': (
                'app/css/site.css',
                'app/css/bootstrap.css',
            ),
            'output_filename': 'app/css/app-layout.min.css',
        },
        'app-readme': {
            'source_filenames': (
                'app/content/app-readme.css',
            ),
            'output_filename': 'app/content/app-readme.min.css',
        },
        'blast-results': {
            'source_filenames': (
                'blast/css/codemirror.css',
                'blast/css/xq-light.css',
                'blast/css/kendo.common-bootstrap.core.css',
                'blast/css/kendo.bootstrap.css',
                'blast/css/jquery-ui-custom.css',
                'blast/css/jquery.dataTables.css',
                'blast/css/dataTables.scroller.css',
                'blast/css/colReorder.dataTables.css',
                'blast/css/dataTables.bootstrap.css',
                'blast/css/bootstrap-select.css',
                'blast/css/bootstrap-switch.css',
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
        'hmmer-css': {
            'source_filenames': (
                'hmmer/css/main.css',
            ),
            'output_filename': 'hmmer/css/hmmer-css.min.css',
        },
        '404-css': {
            'source_filenames': (
                'app/css/404.css',
            ),
            'output_filename': 'app/css/404-css.min.css',
        }
    },
    'JAVASCRIPT': {
        'app-analytics': {
            'source_filenames': (
                'app/scripts/analytics.js',
            ),
            'output_filename': 'app/scripts/app-analytics.min.js',
        },
        'app-layout': {
            'source_filenames': (
                'app/scripts/jquery.js',
                'app/scripts/bootstrap.js',
                'app/scripts/respond.src.js',
                'app/scripts/underscore.js',
                'app/scripts/error.js',
            ),
            'output_filename': 'app/scripts/app-layout.min.js',
        },
        'app-readme': {
            'source_filenames': (
                'app/scripts/marked.min.js',
                'app/scripts/jquery.gh-readme.js'
            ),
            'output_filename': 'app/scripts/app-readme.min.js',
        },
        'blast-results': {
            'source_filenames': (
                'blast/scripts/error.js',
                'blast/scripts/d3.js',
                'blast/scripts/chroma.js',
                'blast/scripts/codemirror.js',
                'blast/scripts/active-line.js',
                'blast/scripts/searchcursor.js',
                'blast/scripts/kendo-hotdogee.js',
                'blast/scripts/jquery-ui.js',
                'blast/scripts/dragscrollable.js',
                'blast/scripts/jquery.dataTables-hotdogee.js',
                'blast/scripts/dataTables.scroller.js',
                'blast/scrtips/dataTables.colReorder.js',
                'blast/scripts/dataTables.tableTools.js',
                'blast/scripts/dataTables.bootstrap.js',
                'blast/scripts/backbone.js',
                'blast/scripts/scribl.1.1.5-hotdogee.js',
                'blast/scripts/bootstrap-select-hotdogee.js',
                'blast/scripts/bootstrap-switch.js',
                'blast/scripts/blast-results.js',
            ),
            'output_filename': 'blast/scripts/blast-results.min.js',
        },
        'blast-js': {
            'source_filenames': (
                'blast/scripts/jquery.hoverIntent.js',
                'blast/scripts/jquery.validate.js',
                'blast/scripts/blast-multi.js',
            ),
            'output_filename': 'blast/scripts/blast-js.min.js',
        },
        'clustal-js': {
            'source_filenames': (
                'clustal/scripts/jquery.hoverIntent.js',
                'clustal/scripts/jquery.validate.js',
                'clustal/scripts/clustal-multi.js',
            ),
            'output_filename': 'clustal/scripts/clustal-js.min.js',
        },
        'hmmer-js': {
            'source_filenames': (
                'hmmer/scripts/jquery.hoverIntent.js',
                'hmmer/scripts/jquery.validate.js',
                'hmmer/scripts/hmmer-multi.js',
            ),
            'output_filename': 'hmmer/scripts/hmmer-js.min.js',
        },
    },
}

if not DEBUG:
    STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
    PIPELINE['PIPELINE_ENABLED'] = True
PIPELINE['CSSMIN_BINARY'] = 'cssmin'
PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.jsmin.JSMinCompressors'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


try:
    HOSTNAME = socket.gethostname()
except:
    HOSTNAME = 'localhost'


# Use settings for production
USE_PROD_SETTINGS = False
if USE_PROD_SETTINGS:
    from settings_prod import *

sys.path.append('%s/misc' % path.dirname(path.abspath(path.dirname(__file__))))
