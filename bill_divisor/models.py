# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User')
