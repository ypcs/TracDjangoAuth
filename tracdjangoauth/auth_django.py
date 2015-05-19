# -*- coding: utf-8 -*-
#
# TracDjangoAuth - Trac Authentication against Django's userdb
# Copyright (c) 2011 Ville Korhonen <ville@xd.fi>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.

"""TracDjangoAuth
Trac Authentication against Django's userdb"""


import os

from trac.core import Component, implements
from trac.config import Option

from acct_mgr.api import IPasswordStore

try:
    from acct_mgr.api import _
except ImportError:
    _ = lambda x: x

# Specify your Django project in the DJANGO_SETTINGS_MODULE 
# environment varible and ensure it is in the PYTHONPATH.
#
# Refer to the instructions for 
# mod_python/mod_wsgi/tracd/<your webserver>
# on how to set environment variables.
#
if os.environ.has_key('DJANGO_SETTINGS_MODULE'):
    __import__(os.environ['DJANGO_SETTINGS_MODULE'])

import django
from django import db

## This does not work with a custom user model:
## # from django.contrib.auth.models import User
## so we try the newer api first and fall back to
## the old fixed User import if that fails
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    username_field = User.USERNAME_FIELD
except ImportError:
    from django.contrib.auth.models import User
    username_field = 'username'

from django.db.models import Q

# initialize Django 1.7+
if hasattr(django, 'setup'):
    django.setup()

class DjangoPasswordStore(Component):
    """Manages user accounts stored in Django's database (User-models).

    To use this implementation add the following configuration section to
    trac.ini.

    {{{
    [account-manager]
    password_store = DjangoPasswordStore
    django_settings_module = myproject.settings
    django_require_group = Trac
    }}}

    django_require_group is optional, it specifies which Django group \
    user must belong to be able to login
    """
    implements(IPasswordStore)
    settings_module = Option('account-manager', 'django_settings_module', '', \
        doc=_("Name of Django settings module"))

    require_group = Option('account-manager', 'django_require_group', '', \
        doc=_("Name of required Django group"))

    def has_user(self, user):
        # TODO
        raise NotImplementedError
        #return user in self.get_users()

    def get_users(self):
        """Returns list of available users

        """
        # TODO
        self.log.debug('acct_mgr: getting user list...')
        raise NotImplementedError
        #return []

    def set_password(self, user, password, old_password=None):
        """Sets user password"""
        self.log.debug('acct_mgr: setting password...')
        duser = self._get_user(user=user, password=old_password)
        if duser:
            duser.set_password(password)
            duser.save()
            return True
        return False

    def delete_user(self, user):
        """Deletes specified user from Django's userdb"""
        self.log.debug('acct_mgr: deleting user...')
        raise NotImplementedError
        #duser = self._get_user(user=user)
        #if duser:
        #    duser.delete()
        #    return True
        #return False

    def _get_user(self, user, password=None):
        """Gets specified user from Django's userdb
 
        If setting django_required_group is defined, user MUST
                be in that group
        If password is specified, also checks it.
        
        Returns User object if user is found (optionally: AND
                belongs to specified group) (optionally: AND
                if password is correct)
        Returns None if user is not found OR error occurs
        Returns False if user is found, but password is incorrect OR
                user doesn't belong to required group
        """
        db.reset_queries()
        try:
            try:
                duser = User.objects.get(Q(is_active=True) & \
                    (Q(**{username_field: user}) | Q(email=user)))
                group = str(self.require_group)
                if group != "":
                    if duser.groups.filter(name=group).count() == 0:
                        return False
                if password and duser.check_password(password):
                    return duser
                elif password is None:
                    return duser
                else:
                    return False
            except User.DoesNotExist:
                return None
        finally:
            db.connection.close()
        return None

    def check_password(self, user, password):
        """Checks user password from Django's userdb"""
        self.log.debug('acct_mgr: checking password...')
        duser = self._get_user(user=user, password=password)

        if duser:
            self.log.debug('acct_mgr: user %s authenticated' % user)
            return True
        else:
            self.log.debug('acct_mgr: user %s NOT authenticated' % user)
            return False
