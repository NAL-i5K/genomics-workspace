from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import Http404
import sys
import logging
from django.core.mail import send_mail

import misc.fileline as src
from misc.logger import i5kLogger

dash = i5kLogger()

#@login_required
def dashboard(request):

    dash.debug("<debug message> %s" % src.request(request))

    dash.info("<info message>")

    dash.warn("<warn message>")

    dash.error("<error message>")

    dash.critical("<critical message>")

    raise Http404("No way Jose")
    #return render(request, 'dashboard/index.html', { 'year': datetime.now().year, 'title': 'Dashboard', })

