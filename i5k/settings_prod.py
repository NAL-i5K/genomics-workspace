DEBUG = False

USE_CACHE = True

with open('/path/to/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

ALLOWED_HOSTS = (
    '.example.com',
)

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
