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
from presentation.models import Spectacle
from django.http import HttpResponseRedirect


def index(request):
    user = request.user

    if user.is_staff:
        spectacles = Spectacle.objects.all()
        c = { 'spectacles':spectacles }
        return render(request, 'index.html', c)
    else:
        return HttpResponseRedirect('/login/')


def my_custom_404_view(request):
    return HttpResponseRedirect('/login/')
