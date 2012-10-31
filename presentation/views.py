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
from django.forms.formsets import formset_factory
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.conf import settings
from presentation.models import Command, EasyMode, Spectacle, HardMode, \
                                Actor, Scene, ChosenCommand, HardModeDuration,\
                                HardModeMessage, LoggedUser, SpectacleArchive
from presentation.models import SPECTACLE_MODE_EASY, SPECTACLE_MODE_HARD
from presentation.forms import EasyModeForm, HardModeForm, HardModeMessageForm
from collections import defaultdict
from PIL import Image
import math


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

            total_logged_users = LoggedUser.objects.all().count()
            minimum = int(math.ceil(total_logged_users * 0.1))

            if total_scene_command >= minimum and not has_cc:
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

    HardModeFormSet = formset_factory(HardModeForm, extra=1, max_num=3)
    formset = HardModeFormSet(initial=[ {'user': user.id,
                                         'spectacle': spectacle.id},
                                        {'user': user.id,
                                         'spectacle': spectacle.id},
                                        {'user': user.id,
                                         'spectacle': spectacle.id}])

    hard_mode_message_form = HardModeMessageForm()
    hard_mode_message_form.fields['spectacle'].widget = HiddenInput(
        attrs={'value':spectacle.id})

    c = {  'commands':commands, 'spectacle':spectacle, 'actors':actors,
           'hard_mode_message_form':hard_mode_message_form,
           'formset': formset }

    return render(request, 'hardmode.html', c)

@login_required
def hard_add(request, s_id):
    user = request.user

    post = request.POST.copy()

    post['form-0-player'] = user.id
    post['form-1-player'] = user.id
    post['form-2-player'] = user.id

    # FIXME
    spectacle = get_object_or_404(Spectacle, pk=s_id)

    post['form-0-spectacle'] = spectacle.id
    post['form-1-spectacle'] = spectacle.id
    post['form-2-spectacle'] = spectacle.id

    try:
        scene = Scene.objects.get(spectacle=spectacle,
                                  status=True,
                                  mode=spectacle.mode)
        post['form-0-scene'] = scene.id
        post['form-1-scene'] = scene.id
        post['form-2-scene'] = scene.id
    except Scene.DoesNotExist:
        alert =  'Oops try again'
        message = simplejson.dumps( { 'error': 1, 'msg': alert } )
        return HttpResponse(message, mimetype="application/json")

    HardModeFormSet = formset_factory(HardModeForm)
    formset = HardModeFormSet(post or None)

    if request.POST and formset.is_valid() and spectacle.mobile_interaction:
        for form in formset.forms:
            form.save()

        message = simplejson.dumps( { 'error': 0 } )
        return HttpResponse(message, mimetype="application/json")
    else:
        message = simplejson.dumps( { 'error': 1 } )
        return HttpResponse(message, mimetype="application/json")

@login_required
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
    if spectacle.mode == SPECTACLE_MODE_EASY:
        commands = spectacle.easy_commands.all()
    else:
        commands = spectacle.hard_commands.all()

    c = { 'spectacle':spectacle, 'commands':commands }

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

def get_chosen_commands_total(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    commands = ChosenCommand.objects.filter(spectacle=spectacle,
                                            mode = spectacle.mode)
    commands = commands.values('command__name', 'command__pk')
    commands = commands.annotate(Count('pk'))

    if spectacle.mode == SPECTACLE_MODE_EASY:

        message = simplejson.dumps( {'error': 0,
                                     'commands': [ {'name': m['command__name'],
                                                    'pk': m['command__pk'],
                                                    'total': m['pk__count'] }
                                                    for m in commands ] })
    else:
        actors = []
        for a in Actor.objects.all():
           commands = a.chosencommand_set.all()
           commands = commands.values('command__name', 'command__pk')
           commands = commands.annotate(Count('pk'))

           if commands:
               actors.append ( { 'pk': a.pk,
                                 'name': a.name,
                                 'commands': [ {'name': m['command__name'],
                                                'pk': m['command__pk'],
                                                'total': m['pk__count'] }
                                                for m in commands ] })

        message = simplejson.dumps( { 'error': 0, 'actors': actors })

    return HttpResponse(message, mimetype="application/json")

def get_chosen_commands(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    if spectacle.mode == SPECTACLE_MODE_EASY:
        commands = ChosenCommand.objects.filter(spectacle=spectacle,
                                                mode = spectacle.mode)

        message = simplejson.dumps( { 'error': 0,
                                      'commands': [ { 'name': c.command.name,
                                                      'command_pk':c.command.pk,
                                                      'pk': c.pk }
                                                      for c in commands ] })
    else:
        actors = []
        for a in Actor.objects.all():
           commands = a.chosencommand_set.all()
           if commands:
               actors.append ( { 'pk': a.pk,
                                 'name': a.name,
                                 'commands': [ { 'name': c.command.name,
                                                  'pk': c.pk }
                                                  for c in commands ] })

        message = simplejson.dumps( { 'error': 0, 'actors': actors })

    return HttpResponse(message, mimetype="application/json")

def frontal_projection_chosen_commands(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)

    try:
        scene = Scene.objects.filter(spectacle=spectacle, mode=spectacle.mode)
        scene = scene.latest('date_created')
    except Scene.DoesNotExist:
        alert =  'Oops try again'
        message = simplejson.dumps( { 'error': 1, 'msg': alert } )
        return HttpResponse(message, mimetype="application/json")

    actors = []
    msg = ''

    if spectacle.mode == SPECTACLE_MODE_EASY:

        try:
            cc = ChosenCommand.objects.get(spectacle = spectacle,
                                           mode = spectacle.mode,
                                           scene = scene)
        except ChosenCommand.DoesNotExist:
            message = simplejson.dumps( { 'error': 1 })
            return HttpResponse(message, mimetype="application/json")

        mode = EasyMode.objects.filter(spectacle=spectacle,
                                       command=cc.command)

        # FIXME
        total = mode.count()
        if total > 0:
            player1 = mode[0].player
            command_name = mode[0].command.name
            if total == 1:
                msg = "%s escolheu %s" % (player1, command_name)
            elif total == 2:
                player2 = mode[1].player
                msg = "%s e %s escolheram %s" % (player1, player2, command_name)
            elif total > 2:
                player2 = mode[1].player
                num = total - 2
                aux = "pessoa" if num == 1 else "pessoas"
                msg = "%s, %s e mais %d %s escolheram %s" % (player1,
                                                             player2,
                                                             num,
                                                             aux,
                                                             command_name)
    else:

        cc = ChosenCommand.objects.filter(spectacle = spectacle,
                                          mode = spectacle.mode,
                                          scene = scene)

        for chosen in cc:
           actors.append({'actor': {'pk': chosen.actor.pk,
                                    'name': chosen.actor.name },
                          'command': { 'name': chosen.command.name }})


    message = simplejson.dumps( { 'error': 0, 'msg': msg, 'actors':actors })
    return HttpResponse(message, mimetype="application/json")

@staff_member_required
def set_hard_chosen_commands(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)

    try:
        scene = Scene.objects.get(spectacle=spectacle,
                                  status=True,
                                  mode=spectacle.mode)
    except Scene.DoesNotExist:
        alert =  'Oops try again'
        message = simplejson.dumps( { 'error': 1, 'msg': alert } )
        return HttpResponse(message, mimetype="application/json")

    actors = []
    for a in Actor.objects.all():
        commands = a.hardmode_set.filter(spectacle=spectacle, scene=scene)
        if commands:
            commands = commands.values('command__pk', 'command__name')
            commands = commands.annotate(total=Count('command__pk'))

            # FIXME
            max_value = 0
            command_id = None
            for c in commands:
                if c['total'] > max_value:
                    max_value = c['total']
                    command_id = c['command__pk']

            command = Command.objects.get(pk = command_id)

            cc = ChosenCommand(spectacle = spectacle,
                               scene = scene,
                               command = command,
                               mode = spectacle.mode,
                               actor = a)
            cc.save()

            actors.append ({ 'actor': { 'name':a.name,
                                         'pk': a.pk },
                             'command': { 'name':command.name,
                                          'pk': command.pk } })

        else:
            # FIXME
            actors.append ({ 'actor': { 'name':a.name,
                                        'pk': a.pk },
                             'command': { 'name': '',
                                          'pk': '' } })

    # FIXME Counter is only in pyhton2.7
    # from django.db.models import Counter
    # total_cc = len(Counter(actor['command']['pk'] for actor in actors))

    total = defaultdict(int)
    for actor in actors:
        total[actor['command']['pk']] += 1
    total_cc = len(total)

    if total_cc == 3:
        spectacle.hard_happiness_meter += 15
    elif total_cc == 2:
        spectacle.hard_happiness_meter -= 5
    elif total_cc == 1:
        spectacle.hard_happiness_meter -= 15
    spectacle.save()

    message = simplejson.dumps( { 'error': 0, 'actors':actors })
    return HttpResponse(message, mimetype="application/json")

@staff_member_required
def controller(request, s_id):

    spectacle = get_object_or_404(Spectacle, pk=s_id)

    files = SpectacleArchive.objects.filter(spectacle=spectacle,
                                            mode=spectacle.mode)

    duration = HardModeDuration.objects.filter(spectacle=spectacle)

    c = { 'spectacle':spectacle, 'hard_duration':duration, 'files': files }

    return render(request, "controller.html", c)

@staff_member_required
def set_mobile_interaction(request, s_id):

    spectacle = get_object_or_404(Spectacle, pk=s_id)
    if spectacle.mobile_interaction:
        # Close
        try:
            mi = False
            scene = Scene.objects.get(spectacle=spectacle,
                                      status=True,
                                      mode=spectacle.mode)

            scene.status = mi
            scene.save()
        except Scene.DoesNotExist:
            message = simplejson.dumps( { 'error': 1 } )
            return HttpResponse(message, mimetype="application/json")
    else:
        # Open
        mi = True
        scene = Scene(mode=spectacle.mode, spectacle=spectacle, status=mi)
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

@staff_member_required
def decrease_happiness(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    if spectacle.mode == SPECTACLE_MODE_EASY:
        spectacle.easy_happiness_meter -= 10
        value = spectacle.easy_happiness_meter
    else:
        spectacle.hard_happiness_meter -= 30
        value = spectacle.hard_happiness_meter

    spectacle.save()
    message = simplejson.dumps( { 'error': 0,
                                  'happiness_value': value })
    return HttpResponse(message, mimetype="application/json")

@staff_member_required
def reset_spectacle(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    spectacle.mode = SPECTACLE_MODE_EASY
    spectacle.easy_happiness_meter = 50
    spectacle.hard_happiness_meter = 50
    spectacle.mobile_interaction = False
    spectacle.scene_set.all().delete()
    spectacle.save()
    LoggedUser.objects.all().delete()
    for sa in SpectacleArchive.objects.filter(spectacle=spectacle):
        sa.show = False
        sa.save()
    message = simplejson.dumps( { 'error': 0 })
    return HttpResponse(message, mimetype="application/json")

def get_last_hard_message(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)

    try:
        msg = HardModeMessage.objects.filter(spectacle=spectacle)
        msg = msg.latest('date_created')
    except HardModeMessage.DoesNotExist:
        message = simplejson.dumps( { 'error': 1 } )
        return HttpResponse(message, mimetype="application/json")

    message = simplejson.dumps( { 'error': 0,
                                  'msg': {'pk': msg.pk, 'text': msg.message} })
    return HttpResponse(message, mimetype="application/json")

def get_last_scene_duration(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    try:
        scene = spectacle.scene_set.get(status=True)
        message = simplejson.dumps({'error': 0,
                                    'scene': {'pk':scene.pk,
                                              'duration':scene.duration,
                                              'show':scene.show_countdown}})
    except Scene.DoesNotExist:
        try:
            scene = spectacle.scene_set.latest('date_created')
            message = simplejson.dumps({'error': 0,
                                        'scene': {'pk':scene.pk,
                                                  'duration':scene.duration,
                                                  'show':scene.show_countdown}})
        except Scene.DoesNotExist:
            message = simplejson.dumps( { 'error': 1 } )

    return HttpResponse(message, mimetype="application/json")

@staff_member_required
def set_last_scene_duration(request, s_id):

    duration = request.POST['duration']
    if duration:
        spectacle = get_object_or_404(Spectacle, pk=s_id)
        if spectacle.mobile_interaction:
            try:
                scene = Scene.objects.get(spectacle=spectacle,
                                          status=True,
                                          mode=spectacle.mode)
                scene.duration = int(duration)
                scene.show_countdown = True
                scene.save()
            except Scene.DoesNotExist:
                message = simplejson.dumps( { 'error': 1 } )
                return HttpResponse(message, mimetype="application/json")
    else:
        message = simplejson.dumps( { 'error': 1 } )
        return HttpResponse(message, mimetype="application/json")

    message = simplejson.dumps( { 'error': 0 })
    return HttpResponse(message, mimetype="application/json")

@staff_member_required
def set_countdown_displayed(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    if spectacle.mobile_interaction:
        try:
            scene = Scene.objects.get(spectacle=spectacle,
                                      status=True,
                                      mode=spectacle.mode)
            scene.show_countdown = False
            scene.save()
        except Scene.DoesNotExist:
            message = simplejson.dumps( { 'error': 1 } )
            return HttpResponse(message, mimetype="application/json")

    message = simplejson.dumps( { 'error': 0 })
    return HttpResponse(message, mimetype="application/json")

@staff_member_required
def change_spectacle_mode(request, s_id):

    spectacle = get_object_or_404(Spectacle, pk=s_id)

    if spectacle.mode == SPECTACLE_MODE_EASY:
        spectacle.mode = SPECTACLE_MODE_HARD
        spectacle.mobile_interaction = False
        spectacle.save()
        for scene in spectacle.scene_set.filter(status=True):
            scene.status = False
            scene.save()

        message = simplejson.dumps( { 'error': 0 })
    else:
        message = simplejson.dumps( { 'error': 1 })

    return HttpResponse(message, mimetype="application/json")

def get_spectable_mode(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    message = simplejson.dumps( { 'error': 0, 'mode':spectacle.mode })
    return HttpResponse(message, mimetype="application/json")

@receiver(user_logged_in)
def login_user(sender, request, user, **kwargs):
    try:
        u = LoggedUser.objects.get(player=user)
    except LoggedUser.DoesNotExist:
        if not user.is_staff:
            u = LoggedUser(player=user)
            u.save()

@receiver(user_logged_out)
def logout_user(sender, request, user, **kwargs):
    if user:
        try:
            u = LoggedUser.objects.get(player=user)
            u.delete()
        except LoggedUser.DoesNotExist:
            pass

def backside_projection_show(request, s_id):

    spectacle = get_object_or_404(Spectacle, pk=s_id)

    c = { 'spectacle':spectacle }

    return render(request, 'backsite_projection.html', c)

def get_backside_projection_content(request, s_id):

    spectacle = get_object_or_404(Spectacle, pk=s_id)

    try:
        sa = SpectacleArchive.objects.get(spectacle=spectacle,
                                               mode=spectacle.mode,
                                               show=True)
        url = "%s%s" % (settings.STATIC_URL, sa.archive.url)

        try:
            img = Image.open(sa.archive.path).verify()
            archive_type = 'image'
        except Exception:
            archive_type = 'video'

        message = simplejson.dumps( { 'error': 0,
                                      'file': url,
                                      'archive_type': archive_type })

    except SpectacleArchive.DoesNotExist:
        message = simplejson.dumps( { 'error': 1  })

    return HttpResponse(message, mimetype="application/json")

@staff_member_required
def set_backside_projection_content(request, s_id):

    spectacle = get_object_or_404(Spectacle, pk=s_id)

    # FIXME
    id_archive = request.POST['id_archive']
    if id_archive:
        for sa in SpectacleArchive.objects.all():
            sa.show = False
            sa.save()
        try:
            sa = SpectacleArchive.objects.get(pk = int(id_archive),
                                              spectacle = spectacle,
                                              mode = spectacle.mode)
            sa.show = True
            sa.save()
            message = simplejson.dumps( { 'error': 0  })
        except SpectacleArchive.DoesNotExist:
            message = simplejson.dumps( { 'error': 1  })
    else:
        message = simplejson.dumps( { 'error': 1  })

    return HttpResponse(message, mimetype="application/json")

def monitor_show(request, s_id):
    spectacle = get_object_or_404(Spectacle, pk=s_id)
    c = { 'spectacle': spectacle }
    return render(request, 'monitor.html', c)
