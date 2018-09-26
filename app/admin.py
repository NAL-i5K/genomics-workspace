from __future__ import absolute_import
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import ModelForm
from suit.widgets import AutosizedTextarea
from app.models import Organism


class OrganismForm(ModelForm):
    class Meta:
        widgets = {
            'description': AutosizedTextarea(attrs={'rows': 10, 'class': 'input-xxlarge'}),
        }


class OrganismAdmin(admin.ModelAdmin):
    form = OrganismForm
    list_display = ('display_name', 'short_name', 'tax_id', 'short_description',)
    search_fields = ('display_name', 'short_name', 'tax_id', 'description',)
    actions_on_top = True
    actions_on_bottom = True

    def short_description(self, obj):
        if len(obj.description) < 100:
            return obj.description
        else:
            return obj.description[:100] + '...'
    short_description.short_description = 'description'

    class Media:
        css = {
            'all': ('app/css/organism-admin.css',)
        }
        js = ('app/scripts/organism-admin.js',)


admin.site.register(Organism, OrganismAdmin)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
