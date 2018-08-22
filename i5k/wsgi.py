"""
WSGI config for i5k project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "i5k.settings")

if settings.USE_VIRTUALENV:
    import sys
    import site

    BASE_DIR = settings.BASE_DIR
    VIRTUALENV_ROOT = settings.VIRTUALENV_ROOT

    # Add the site-packages of the chosen virtualenv to work with
    python_version = sys.version[0:3]  # ex: two digit python versions, like 2.7, 3.5
    site.addsitedir(os.path.join(BASE_DIR, VIRTUALENV_ROOT, 'lib/python' + python_version + '/site-packages'))

    # Add the app's directory to the PYTHONPATH
    sys.path.append(BASE_DIR)
    sys.path.append(os.path.join(BASE_DIR, 'i5k'))

    # Activate your virtual env
    activate_env=os.path.expanduser(os.path.join(BASE_DIR, VIRTUALENV_ROOT, 'bin/activate_this.py'))
    execfile(activate_env, dict(__file__=activate_env))

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
