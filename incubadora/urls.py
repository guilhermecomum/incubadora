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

    # users
    (r'^login/', 'users.views.user_login'),
    (r'^logout/', 'users.views.user_logout'),

)

urlpatterns += patterns('presentation.views',

    # Spectacle

    url(r'^spectacle/(?P<s_id>(.*))/mode/$',
        'get_spectable_mode',
        name='get-spectable-mode'),

    # Hard
    url(r'^hard/spectacle/(?P<s_id>(.*))/$', 'hard_show', name='hard-show'),

    url(r'^hard/command/add/(?P<s_id>(.*))/$', 'hard_add', name='hard-add'),

    url(r'^hard/message/add/(?P<s_id>(.*))/$',
        'hard_message_add',
        name='hard-message-add'),

    # Easy
    url(r'^easy/spectacle/(?P<s_id>(.*))/$', 'easy_show', name='easy-show'),

    url(r'^easy/command/add/(?P<s_id>(.*))/$', 'easy_add', name='easy-add',),

    # Frontal Projection

    url(r'^frontal-projection/(?P<s_id>(.*))/get/draw-list-bullet/$',
        'frontal_projection_draw_list_bullet',
        name='frontal-projection-draw-list-bullet'),

    url(r'^frontal-projection/(?P<s_id>(.*))/set/countdown-displayed/$',
        'set_countdown_displayed',
        name='set-countdown-displayed'),

    url(r'^frontal-projection/(?P<s_id>(.*))/get/lastmessage/$',
        'get_last_hard_message',
        name='get-last-hard-message'),

    url(r'^frontal-projection/(?P<s_id>(.*))/$',
        'frontal_projection',
        name='frontal-projection-show'),

    # Commands

    url(r'^commands/(?P<s_id>(.*))/$', 'get_commands', name='get-commands'),

    # Chosen commands

    url(r'^chosen-commands/(?P<s_id>(.*))/get/$',
        'show_chosen_commands',
        name='show-chosen-commands'),

    url(r'^chosen-commands/(?P<s_id>(.*))/total/$',
        'get_chosen_commands_total',
        name='get-chosen-commands-total'),

    url(r'^chosen-commands/(?P<s_id>(.*))/$',
        'get_chosen_commands',
        name='get-chosen-commands'),

    url(r'^set-hard-chosen-commands/(?P<s_id>(.*))/$',
        'set_hard_chosen_commands',
        name='set-hard-chosen-commands'),

    # Happiness Meter

    url(r'^happiness-meter/(?P<s_id>(.*))/$',
        'happiness_meter',
        name='happiness-meter'),

    url(r'^decrease-happiness/(?P<s_id>(.*))/$',
        'decrease_happiness',
        name='decrease-happiness'),

     # Controller

     url(r'^controller/(?P<s_id>(.*))/change-spectacle-mode/$',
         'change_spectacle_mode',
         name='change-spectacle-mode'),

     url(r'^controller/(?P<s_id>(.*))/set/last-scene-duration/$',
         'set_last_scene_duration',
         name='set-last-scene-duration'),

     url(r'^controller/(?P<s_id>(.*))/get/last-scene-duration/$',
         'get_last_scene_duration',
         name='get-last-scene-duration'),

     url(r'^controller/(?P<s_id>(.*))/set/mobile-interaction/$',
         'set_mobile_interaction',
         name='set-mobile-interaction'),

    url(r'^controller/(?P<s_id>(.*))/mobile-interaction/$',
         'get_mobile_interaction',
         name='get-mobile-interaction'),

     url(r'^controller/(?P<s_id>(.*))/reset/spectacle/$',
         'reset_spectacle',
         name='reset-spectacle'),

     url(r'^controller/(?P<s_id>(.*))/$', 'controller', name='controller'),

    # Backside Projection

     url(r'^backside-projection/(?P<s_id>(.*))/set/content/$',
         'set_backside_projection_content',
         name='set-backside-projection-content'),

     url(r'^backside-projection/(?P<s_id>(.*))/get/content/$',
         'get_backside_projection_content',
         name='get-backside-projection-content'),

     url(r'^backside-projection/(?P<s_id>(.*))/$',
         'backside_projection_show',
         name='backside-projection-show'),

    # Monitor

     url(r'^monitor/(?P<s_id>(.*))/$', 'monitor_show', name='monitor-show'),

)
