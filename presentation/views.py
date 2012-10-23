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

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.utils import simplejson
from django.forms.widgets import HiddenInput
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from presentation.models import Command, EasyMode, Spectacle, HardMode, \
                                Actor, Scene, ChosenCommand
from presentation.models import SPECTACLE_MODE_EASY, SPECTACLE_MODE_HARD
from presentation.forms import EasyModeForm, HardModeForm, HardModeMessageForm


MAX_SAME_COMMAND = 3


@login_required
def easy_show(request, s_id):
    user = request.user
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    commands = spectacle.easy_commands.all()

    form = EasyModeForm()
    form.fields['player'].widget = HiddenInput(attrs={'value':user.id})
    form.fields['spectacle'].widget = HiddenInput(attrs={'value':spectacle.id})

    c = { 'form':form, 'commands':commands, 'spectacle':spectacle }

    return render(request, 'easymode.html', c)

@login_required
def easy_add(request, s_id):
    user = request.user

    post = request.POST.copy()
    post['player'] = user.id

    spectacle = get_object_or_404(Spectacle, pk=s_id)
    post['spectacle'] = spectacle.id

    try:
        scene = Scene.objects.get(spectacle=spectacle,
                                  status=True,
                                  mode=spectacle.mode)
        post['scene'] = scene.id
    except Scene.DoesNotExist:
        alert =  'Oops try again'
        message = simplejson.dumps( { 'error': 1, 'error-msg': alert } )
        return HttpResponse(message, mimetype="application/json")

    form = EasyModeForm(post or None)

    if request.POST and form.is_valid():
        instance = form.save(commit=False)
        command = instance.command
        total_cc = ChosenCommand.objects.filter(spectacle = spectacle,
                                                command = command,
                                                mode = spectacle.mode).count()

        if total_cc < MAX_SAME_COMMAND and spectacle.mobile_interaction:
            total_scene_command = EasyMode.objects.filter(spectacle = spectacle,
                                                          scene = scene,
                                                          command = command)
            total_scene_command = total_scene_command.count()

            has_cc = ChosenCommand.objects.filter(spectacle = spectacle,
                                                  scene = scene).count()

            if total_scene_command == 1 and not has_cc:
                cc = ChosenCommand(spectacle = spectacle,
                                   scene = scene,
                                   command = command,
                                   mode = spectacle.mode)
                cc.save()

            if total_cc == 0:
                spectacle.easy_happiness_meter += 5
            elif total_cc == 1:
                spectacle.easy_happiness_meter += 5
            elif total_cc == 2:
                spectacle.easy_happiness_meter += 5

            instance.save()
            spectacle.save()
            message = simplejson.dumps( { 'error': 0 } )
            return HttpResponse(message, mimetype="application/json")

        else:
            message = simplejson.dumps( { 'error': 1,
                                          'error-msg': 'max-same-command',
                                          'command': [ {'name': command.name,
                                                        'pk': command.pk } ] } )
            return HttpResponse(message, mimetype="application/json")
    else:
        message = simplejson.dumps( { 'error': 1 } )
        return HttpResponse(message, mimetype="application/json")

def happiness_meter(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    if spectacle.mode == SPECTACLE_MODE_EASY:
        value = spectacle.easy_happiness_meter
    else:
        value = spectacle.hard_happiness_meter
    message = simplejson.dumps( { 'error': 0, 'value':value } )
    return HttpResponse(message, mimetype="application/json")

@login_required
def hard_show(request, s_id):
    user = request.user
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    commands = spectacle.hard_commands.all()
    actors = Actor.objects.filter(spectacle=spectacle).all()

    hard_mode_form = HardModeForm()
    hard_mode_form.fields['player'].widget = HiddenInput(
        attrs={'value':user.id})
    hard_mode_form.fields['spectacle'].widget = HiddenInput(
        attrs={'value':spectacle.id})

    hard_mode_message_form = HardModeMessageForm()
    hard_mode_message_form.fields['spectacle'].widget = HiddenInput(
        attrs={'value':spectacle.id})

    c = { 'hard_mode_form':hard_mode_form, 'commands':commands,
          'spectacle':spectacle, 'actors':actors,
          'hard_mode_message_form':hard_mode_message_form }

    return render(request, 'hardmode.html', c)

@login_required
def hard_add(request, s_id):
    user = request.user

    post = request.POST.copy()
    post['player'] = user.id

    # FIXME
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    try:
        scene = Scene.objects.get(spectacle=spectacle,
                                  status=True,
                                  mode=spectacle.mode)
        post['scene'] = scene.id
    except Scene.DoesNotExist:
        alert =  'Oops try again'
        message = simplejson.dumps( { 'error': 1, 'msg': alert } )
        return HttpResponse(message, mimetype="application/json")

    form = HardModeForm(post or None)

    if request.POST and form.is_valid():
        instance = form.save(commit=False)
        spectacle = get_object_or_404(Spectacle, pk=instance.spectacle.pk)
        if spectacle.mobile_interaction:
            total = HardMode.objects.filter(spectacle = instance.spectacle,
                                            command = instance.command,
                                            actor = instance.actor).count()
            if total == 0:
                spectacle.hard_happiness_meter += 15
            elif total == 1:
                spectacle.hard_happiness_meter -= 5
            elif total == 2:
                spectacle.hard_happiness_meter -= 15

            spectacle.save()
            instance.save()
            message = simplejson.dumps( { 'error': 0 } )
            return HttpResponse(message, mimetype="application/json")
        else:
            message = simplejson.dumps( { 'error': 1 } )
            return HttpResponse(message, mimetype="application/json")
    else:
        message = simplejson.dumps( { 'error': 1 } )
        return HttpResponse(message, mimetype="application/json")

def hard_message_add(request, s_id):
    user = request.user
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    post = request.POST.copy()
    post['player'] = user.id

    form = HardModeMessageForm(post or None)

    if request.POST and form.is_valid():
        instance = form.save()
        spectacle.hard_happiness_meter += 10
        spectacle.save()
        message = simplejson.dumps( { 'error': 0 } )
        return HttpResponse(message, mimetype="application/json")
    else:
        message = simplejson.dumps( { 'error': 1 } )
        return HttpResponse(message, mimetype="application/json")

def frontal_projection(request, s_id):

    spectacle = get_object_or_404(Spectacle, pk=s_id)

    c = { 'spectacle':spectacle }

    return render(request, "frontal_projection.html", c)

def get_commands(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    if spectacle.mode == SPECTACLE_MODE_EASY:
        spectacle_mode = EasyMode.objects.filter(spectacle=spectacle)
    else:
        spectacle_mode = HardMode.objects.filter(spectacle=spectacle)
    spectacle_mode = spectacle_mode.values('command__name', 'command__pk')
    spectacle_mode = spectacle_mode.annotate(Count('pk'))

    message = simplejson.dumps( { 'error': 0,
                                  'commands': [ { 'name': m['command__name'],
                                                  'pk': m['command__pk'],
                                                  'total': m['pk__count'] }
                                                  for m in spectacle_mode ] })

    return HttpResponse(message, mimetype="application/json")

def get_chosen_commands(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    commands = ChosenCommand.objects.filter(spectacle=spectacle,
                                            mode = spectacle.mode)

    message = simplejson.dumps( { 'error': 0,
                                  'commands': [ { 'name': c.command.name,
                                                  'command-pk': c.command.pk,
                                                  'pk': c.pk }
                                                  for c in commands ] })

    return HttpResponse(message, mimetype="application/json")

@staff_member_required
def controller(request, s_id):

    spectacle = get_object_or_404(Spectacle, pk=s_id)

    c = { 'spectacle':spectacle }

    return render(request, "controller.html", c)

@staff_member_required
def set_mobile_interaction(request, s_id):

    spectacle = get_object_or_404(Spectacle, pk=s_id)
    if spectacle.mobile_interaction:
        # Close
        mi = False
        try:
            scene = Scene.objects.get(spectacle=spectacle,
                                      status=True,
                                      mode=spectacle.mode)

            scene.status = False
            scene.save()
        except Scene.DoesNotExist:
            message = simplejson.dumps( { 'error': 1 } )
            return HttpResponse(message, mimetype="application/json")
    else:
        # Open
        mi = True
        scene = Scene(mode=spectacle.mode, spectacle=spectacle, status=True)
        scene.save()

    spectacle.mobile_interaction = mi
    spectacle.save()

    message = simplejson.dumps( { 'error': 0,
                                  'mobile_interaction': mi })

    return HttpResponse(message, mimetype="application/json")

def get_mobile_interaction(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    mi = spectacle.mobile_interaction
    message = simplejson.dumps( { 'error': 0,
                                  'mobile_interaction': mi })
    return HttpResponse(message, mimetype="application/json")
