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

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # admin
     url(r'^admin/', include(admin.site.urls)),

    # index
    url(r'^$', 'index.views.index', name='index'),

)

urlpatterns += patterns('presentation.views',

    # Hard
    url(r'^hard/spectacle/(?P<s_id>(.*))/$', 'hard_show', name='hard-show'),

    url(r'^hard/command/add/(?P<s_id>(.*))/$', 'hard_add', name='hard-add'),

    # Easy
    url(r'^easy/spectacle/(?P<s_id>(.*))/$', 'easy_show', name='easy-show'),

    url(r'^easy/command/add/(?P<s_id>(.*))/$', 'easy_add', name='easy-add',),

    # Frontal Projection

    url(r'^frontal-projection/(?P<s_id>(.*))/$',
        'frontal_projection',
        name='frontal-projection-show'),

    # Commands

    url(r'^commands/(?P<s_id>(.*))/$', 'get_commands', name='get-commands'),

    # Chosen commands

    url(r'^chosen-commands/(?P<s_id>(.*))/$',
        'get_chosen_commands',
        name='get-chosen-commands'),

    # Happiness Meter

    url(r'^happiness-meter/(?P<s_id>(.*))/$',
        'happiness_meter',
        name='happiness-meter'),

     # Controller
     url(r'^controller/(?P<s_id>(.*))/set/mobile-interaction/$',
         'set_mobile_interaction',
         name='set-mobile-interaction'),

    url(r'^controller/(?P<s_id>(.*))/mobile-interaction/$',
         'get_mobile_interaction',
         name='get-mobile-interaction'),

     url(r'^controller/(?P<s_id>(.*))/$', 'controller', name='controller'),

)
