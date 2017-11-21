from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User)
    institution = models.CharField(max_length=100, null=False)


class OrganismManager(models.Manager):
    def get_by_natural_key(self, short_name):
        return self.get(short_name=short_name)


class Organism(models.Model):
    objects = OrganismManager()
    display_name = models.CharField(max_length=200, unique=True, help_text='Scientific or common name') # shown to user
    short_name = models.CharField(max_length=20, unique=True, help_text='This is used for file names and variable names in code') # used in code or filenames
    description = models.TextField(blank=True) # optional
    tax_id = models.PositiveIntegerField('NCBI Taxonomy ID', null=True, blank=True, help_text='This is passed into makeblast') # ncbi tax id

    def natural_key(self):
        return (self.short_name,)

    def __unicode__(self):
        return self.display_name

