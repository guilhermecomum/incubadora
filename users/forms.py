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
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from users.models import UserProfile


class UserForm(forms.ModelForm):

    username = forms.EmailField(label=_("Email"))

    def clean_email(self):
        email = self.cleaned_data['username']
        return email

    def clean_first_name(self):
        if not self.cleaned_data['first_name']:
            raise forms.ValidationError(_("This field is required."))
        return self.cleaned_data['first_name']

    class Meta:
        model = User
        fields = ["first_name", "username"]

class UserProfileForm(forms.ModelForm):

    newsletter = forms.BooleanField(widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        widgets = {
            'user': forms.HiddenInput(),
        }
