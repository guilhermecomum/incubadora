# -*- coding: utf-8 -*-
# Copyright (C) 2012 Marcelo Jorge Vieira <metal@alucinados.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
##

from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.conf import settings
from presentation.models import *
from PIL import Image


class SpectacleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple,
                                 'help_text':''},
    }
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['__str__', 'slug', 'status']

class CommandAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['__str__', 'slug']

class ActorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['__str__', 'slug']

class SpectacleArchiveAdmin(admin.ModelAdmin):
    list_display = ['__str__',  'show_image', 'archive_type']
    list_filter = ['archive_type']

    def show_image(self, obj):
        try:
            img = Image.open(obj.archive.path).verify()
            html = '<img src="%s/%s" width="100" />' % (settings.STATIC_URL,
                                                        obj.archive.url)
        except Exception:
            html = ''

        return mark_safe(html)
    show_image.short_description = _('Thumbnail')
    show_image.allow_tags = True


admin.site.register(Spectacle, SpectacleAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Scene)
admin.site.register(EasyMode)
admin.site.register(HardMode)
admin.site.register(ChosenCommand)
admin.site.register(HardModeMessage)
admin.site.register(HardModeDuration)
admin.site.register(LoggedUser)
admin.site.register(SpectacleArchive, SpectacleArchiveAdmin)
