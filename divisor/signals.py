# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import dispatch

bill_update = dispatch.Signal(providing_args=['bill'])
