from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from filebrowser.fields import FileBrowseField
from django.core.urlresolvers import reverse
import os.path
from django.conf import settings
from blast.models import SearchQuery
import app.models

class SearchForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyModelForm, self).__init__(*args, **kwargs)
        self.fields["db_name"] = json.loads(self.fields["db_name"])

    class Meta:
        model = SearchQuery
        fields = ['program', 'db_name', 'enqueue_date']

        #fields = ['enqueue_date', 'program', 'db_name']


