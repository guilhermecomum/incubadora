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

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext as _
from django.forms.widgets import HiddenInput
from users.forms import UserForm, UserProfileForm
from users.models import UserProfile
from presentation.models import Spectacle
from presentation.models import SPECTACLE_MODE_EASY, SPECTACLE_MODE_RESET


def user_login(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)

        email = request.POST['username']
        first_name = request.POST['first_name']

        if email and first_name:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                if form.is_valid():
                    user = form.save(commit=False)
                    user.set_password(user.username)
                    user = form.save()

            user = authenticate(username=email, password=email)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    # FIXME
                    post = request.POST.copy()
                    post['user'] = user.id
                    user_profile_form = UserProfileForm(post)
                    if user_profile_form.is_valid():
                        try:
                            profile = user.get_profile()
                        except:
                            aux = UserProfile.objects
                            profile, created = aux.get_or_create(user=user)
                        newsletter = user_profile_form.clean()['newsletter']
                        profile.newsletter = newsletter
                        profile.save()

                    try:
                        spectacle = Spectacle.objects.get(status=True)
                        if spectacle.mode == SPECTACLE_MODE_EASY or \
                           spectacle.mode == SPECTACLE_MODE_RESET:
                            url = spectacle.get_easy_show_url()
                        else:
                            url = spectacle.get_hard_show_url()
                        return HttpResponseRedirect(url)
                    except Spectacle.MultipleObjectsReturned:
                        msg = '<h1>%s</h1>' % _('Spectacle not found')
                        return HttpResponseNotFound(msg)
    else:
        form = UserForm()
        user_profile_form = UserProfileForm()

    c = { 'form':form, 'user_profile_form':user_profile_form }

    return render(request, 'login.html', c)

def user_logout(request):

    logout(request)
    return HttpResponseRedirect('/')
