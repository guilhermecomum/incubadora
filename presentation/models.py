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

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


SPECTACLE_MODE_EASY = '1'
SPECTACLE_MODE_HARD = '2'

MODE_CHOICES = (
    (SPECTACLE_MODE_EASY, u'Easy',),
    (SPECTACLE_MODE_HARD, u'Hard',),
)

class Command(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    slug = models.SlugField(verbose_name=_('Slug'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('Command')
        verbose_name_plural = _('Commands')

    def __unicode__(self):
        return "%s" % (self.name)

class Spectacle(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    slug = models.SlugField(verbose_name=_('Slug'), max_length=100, unique=True)
    status = models.BooleanField(verbose_name=_('Status'), default=False)
    mode = models.CharField(
        verbose_name=_('Mode'),
        max_length=1,
        choices=MODE_CHOICES,
        default='1')
    mobile_interaction = models.BooleanField(
        verbose_name=_('Mobile Interaction'),
        default=False)
    easy_happiness_meter = models.IntegerField(
        verbose_name=_('Easy Happiness Meter'),
        default=50,
        blank=True,
        null=True)
    hard_happiness_meter = models.IntegerField(
        verbose_name=_('Hard Happiness Meter'),
        default=50,
        blank=True,
        null=True)
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        auto_now_add=True)
    easy_commands = models.ManyToManyField(
        Command,
        verbose_name=_('Easy Commands'),
        related_name='easy_commands',
        blank=True,
        null=True)
    hard_commands = models.ManyToManyField(
        Command,
        verbose_name=_('Hard Commands'),
        related_name='hard_commands',
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Spectacle')
        verbose_name_plural = _('Spectacles')

    def __unicode__(self):
        return "%s" % (self.name)

    @models.permalink
    def get_easy_show_url(self):
        return ('easy-show', [str(self.pk)])

    @models.permalink
    def get_hard_show_url(self):
        return ('hard-show', [str(self.pk)])

    @models.permalink
    def get_frontal_projection_show_url(self):
        return ('frontal-projection-show', [str(self.pk)])

    @models.permalink
    def get_happiness_meter_url(self):
        return ('happiness-meter', [str(self.pk)])

    @models.permalink
    def get_commands_url(self):
        return ('get-commands', [str(self.pk)])

    @models.permalink
    def get_chosen_commands_url(self):
        return ('get-chosen-commands', [str(self.pk)])

    @models.permalink
    def get_controller_url(self):
        return ('controller', [str(self.pk)])

    @models.permalink
    def get_mobile_interaction_url(self):
        return ('get-mobile-interaction', [str(self.pk)])

    @models.permalink
    def set_mobile_interaction_url(self):
        return ('set-mobile-interaction', [str(self.pk)])

    @models.permalink
    def easy_add_url(self):
        return ('easy-add', [str(self.pk)])

    @models.permalink
    def hard_add_url(self):
        return ('hard-add', [str(self.pk)])

    @models.permalink
    def hard_message_add_url(self):
        return ('hard-message-add', [str(self.pk)])

    @models.permalink
    def decrease_happiness_url(self):
        return ('decrease-happiness', [str(self.pk)])

    @models.permalink
    def set_hard_chosen_commands_url(self):
        return ('set-hard-chosen-commands', [str(self.pk)])

    @models.permalink
    def reset_spectacle_url(self):
        return ('reset-spectacle', [str(self.pk)])

    @models.permalink
    def get_last_hard_message_url(self):
        return ('get-last-hard-message', [str(self.pk)])

    @models.permalink
    def get_chosen_commands_total_url(self):
        return ('get-chosen-commands-total', [str(self.pk)])

    @models.permalink
    def get_last_scene_duration_url(self):
        return ('get-last-scene-duration', [str(self.pk)])

    @models.permalink
    def set_last_scene_duration_url(self):
        return ('set-last-scene-duration', [str(self.pk)])

    @models.permalink
    def set_countdown_displayed_url(self):
        return ('set-countdown-displayed', [str(self.pk)])

    @models.permalink
    def change_spectacle_mode_url(self):
        return ('change-spectacle-mode', [str(self.pk)])

    @models.permalink
    def get_spectable_mode_url(self):
        return ('get-spectable-mode', [str(self.pk)])

    @models.permalink
    def show_chosen_commands_url(self):
        return ('show-chosen-commands', [str(self.pk)])

    @models.permalink
    def get_backside_projection_show_url(self):
        return ('backside-projection-show', [str(self.pk)])

    @models.permalink
    def get_backside_projection_content_url(self):
        return ('get-backside-projection-content', [str(self.pk)])

    @models.permalink
    def set_backside_projection_content_url(self):
        return ('set-backside-projection-content', [str(self.pk)])

    @models.permalink
    def get_monitor_show_url(self):
        return ('monitor-show', [str(self.pk)])

class Actor(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))
    slug = models.SlugField(verbose_name=_('Slug'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('Actor')
        verbose_name_plural = _('Actors')

    def __unicode__(self):
        return "%s" % (self.name)

class Scene(models.Model):
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))
    status = models.BooleanField(verbose_name=_('Status'), default=True)
    show_countdown = models.BooleanField(
        verbose_name=_('Show Countdown'),
        default=False)
    duration = models.IntegerField(
        verbose_name=_('Duration'),
        blank=True,
        null=True)
    mode = models.CharField(
        verbose_name=_('Mode'),
        max_length=1,
        choices=MODE_CHOICES,
        default='1')
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        auto_now_add=True)
    last_changed = models.DateTimeField(
        verbose_name=_('Last Changed'),
        auto_now=True)

    class Meta:
        verbose_name = _('Scene')
        verbose_name_plural = _('Scenes')

    def __unicode__(self):
        return "%s | %s" % (self.date_created, self.last_changed)

class ChosenCommand(models.Model):
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))
    scene = models.ForeignKey(Scene, verbose_name=_('Scene'))
    command = models.ForeignKey(Command, verbose_name=_('Command'))
    actor = models.ForeignKey(
        Actor,
        verbose_name=_('Actor'),
        blank=True,
        null=True)
    mode = models.CharField(
        verbose_name=_('Mode'),
        max_length=1,
        choices=MODE_CHOICES,
        default='1')

    class Meta:
        verbose_name = _('Chosen Command')
        verbose_name_plural = _('Chosen Commands')

    def __unicode__(self):
        return "%s | %s" % (self.spectacle, self.command)

class EasyMode(models.Model):
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))
    scene = models.ForeignKey(Scene, verbose_name=_('Scene'))
    command = models.ForeignKey(Command, verbose_name=_('Command'))
    player = models.ForeignKey(User, verbose_name=_('Player'))
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        auto_now_add=True)

    class Meta:
        verbose_name = _('Easy Mode')
        verbose_name_plural = _('EasyMode')
        unique_together = ('spectacle', 'scene', 'player')

    def __unicode__(self):
        return "%s | %s | %s" % (self.spectacle, self.command, self.player)

class HardMode(models.Model):
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))
    scene = models.ForeignKey(Scene, verbose_name=_('Scene'))
    actor = models.ForeignKey(Actor, verbose_name=_('Actor'))
    command = models.ForeignKey(Command, verbose_name=_('Command'))
    player = models.ForeignKey(User, verbose_name=_('Player'))
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        auto_now_add=True)

    class Meta:
        verbose_name = _('Hard Mode')
        verbose_name_plural = _('Hard Mode')
        unique_together = ('spectacle', 'actor', 'command', 'player', 'scene')

    def __unicode__(self):
        return "%s | %s | %s" % (self.spectacle, self.command, self.player)

class HardModeMessage(models.Model):
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))
    message = models.CharField(verbose_name=_('Message'), max_length=128)
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        auto_now_add=True)

    class Meta:
        verbose_name = _('Hard Mode Message')
        verbose_name_plural = _('Hard Mode Messages')

    def __unicode__(self):
        return "%s | %s" % (self.spectacle, self.message)

class HardModeDuration(models.Model):
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))
    duration = models.TimeField(verbose_name=_('Duration'))

    class Meta:
        verbose_name = _('Hard Mode Duration')
        verbose_name_plural = _('Hard Mode Duration')

    def __unicode__(self):
        return "%s" % (self.duration)

class LoggedUser(models.Model):
    player = models.ForeignKey(User, verbose_name=_('Player'), unique=True)

    class Meta:
        verbose_name = _('Logged User')
        verbose_name_plural = _('Logged Users')

    def __unicode__(self):
        return "%s" % self.player

class SpectacleArchive(models.Model):
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    archive = models.FileField(verbose_name=_('File'), upload_to='files')
    show = models.BooleanField(verbose_name=_('Show'), default=False)
    mode = models.CharField(
        verbose_name=_('Mode'),
        max_length=1,
        choices=MODE_CHOICES)

    class Meta:
        verbose_name = _('Spectacle File')
        verbose_name_plural = _('Spectacle Files')

    def __unicode__(self):
        return "%s" % self.name
