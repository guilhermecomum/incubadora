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
from users.forms import UserForm
from presentation.models import Spectacle


def user_login(request):

    if request.method == 'POST':
        form = UserForm(request.POST)

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
                    try:
                        spectacle = Spectacle.objects.get(status=True)
                        url = spectacle.get_easy_show_url()
                        return HttpResponseRedirect(url)
                    except Spectacle.MultipleObjectsReturned:
                        msg = '<h1>%s</h1>' % _('Spectacle not found')
                        return HttpResponseNotFound(msg)
    else:
        form = UserForm()

    c = { 'form':form }

    return render(request, 'login.html', c)

def user_logout(request):

    logout(request)
    return HttpResponseRedirect('/')
