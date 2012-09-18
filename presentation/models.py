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

class Spectacle(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
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
        default=0,
        blank=True,
        null=True)
    hard_happiness_meter = models.IntegerField(
        verbose_name=_('Hard Happiness Meter'),
        default=0,
        blank=True,
        null=True)
    receive_commands = models.BooleanField(
        verbose_name=_('Receive Commands'),
        default=False)
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        auto_now_add=True)

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
    def get_hard_happiness_meter_url(self):
        return ('hard-happiness-meter', [str(self.pk)])

    @models.permalink
    def get_hard_happiness_meter_url(self):
        return ('easy-happiness-meter', [str(self.pk)])

    @models.permalink
    def get_frontal_projection_commands_url(self):
        return ('frontal-projection-commands', [str(self.pk)])

class Command(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))

    class Meta:
        verbose_name = _('Command')
        verbose_name_plural = _('Commands')

    def __unicode__(self):
        return "%s" % (self.name)

class Actor(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))

    class Meta:
        verbose_name = _('Actor')
        verbose_name_plural = _('Actors')

    def __unicode__(self):
        return "%s" % (self.name)

class EasyMode(models.Model):
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))
    command = models.ForeignKey(Command, verbose_name=_('Command'))
    player = models.ForeignKey(User, verbose_name=_('Player'))
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        auto_now_add=True)

    class Meta:
        verbose_name = _('Easy Mode')
        verbose_name_plural = _('EasyMode')

    def __unicode__(self):
        return "%s | %s | %s" % (self.spectacle, self.command, self.player)

class HardMode(models.Model):
    spectacle = models.ForeignKey(Spectacle, verbose_name=_('Spectacle'))
    actor = models.ForeignKey(Actor, verbose_name=_('Actor'))
    command = models.ForeignKey(Command, verbose_name=_('Command'))
    player = models.ForeignKey(User, verbose_name=_('Player'))
    message = models.CharField(
        verbose_name=_('Message'),
        max_length=128,
        blank=True,
        null=True)
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        auto_now_add=True)

    class Meta:
        verbose_name = _('Hard Mode')
        verbose_name_plural = _('Hard Mode')

    def __unicode__(self):
        return "%s | %s | %s" % (self.spectacle, self.command, self.player)
