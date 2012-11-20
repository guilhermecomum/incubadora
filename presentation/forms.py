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

from django import forms
from presentation.models import *

class EasyModeForm(forms.ModelForm):

    class Meta:
        model = EasyMode
        widgets = {
            'spectacle': forms.HiddenInput(),
            'scene': forms.HiddenInput(),
            'player': forms.HiddenInput(),
            'command': forms.HiddenInput(),
        }

class HardModeForm(forms.ModelForm):

    class Meta:
        model = HardMode
        widgets = {
            'spectacle': forms.HiddenInput(),
            'scene': forms.HiddenInput(),
            'player': forms.HiddenInput(),
            'command': forms.HiddenInput(),
            'actor': forms.HiddenInput(),
       }

class HardModeMessageForm(forms.ModelForm):

    class Meta:
        model = HardModeMessage
        widgets = {
            'spectacle': forms.HiddenInput(),
            'message': forms.Textarea(
                attrs={'placeholder': u'Mande sua mensagem para a INCUBADORA'})
        }

class FrontalProjectionSettingsForm(forms.ModelForm):

    class Meta:
        widgets = {
            'spectacle': forms.HiddenInput(),
        }
        model = FrontalProjectionSettings
