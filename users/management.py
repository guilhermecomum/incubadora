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

# http://blueapples.livejournal.com/178733.html

from django.db.models.signals import post_syncdb
from django.contrib.auth import models as auth_models
from django.db import connection, transaction

def change_username(sender, **kwargs):
    print 'Alter auth_user table ...'
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE auth_user "
                   "MODIFY username VARCHAR(75) NOT NULL")
    transaction.commit_unless_managed()

post_syncdb.connect(change_username, sender=auth_models)
