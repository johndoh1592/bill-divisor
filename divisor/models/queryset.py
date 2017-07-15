# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class StateQuerySet(models.QuerySet):
    def active_instances(self):
        return self.filter(is_active=True)

    def inactive_instances(self):
        return self.filter(is_active=False)
