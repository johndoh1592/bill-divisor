# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import date
from django.utils.translation import ugettext_lazy as _

from .queryset import StateQuerySet


class Event(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Name'))
    start = models.DateField(verbose_name=_('Start-date'))
    end = models.DateField(blank=True, null=True, verbose_name=_('End-date'))
    is_active = models.BooleanField(default=True)

    objects = StateQuerySet.as_manager()

    def __unicode__(self):
        return self.get_description()

    def get_name(self):
        return self.name

    def get_description(self):
        return '{name} {start}{end}'.format(
            name=self.get_name(),
            start=date(self.start, 'SHORT_DATE_FORMAT'),
            end=' - {}'.format(date(self.end, 'SHORT_DATE_FORMAT')) if self.end else ''
        )

    def get_is_active(self):
        if self.is_active:
            return _('Yes')
        return _('No')

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

    def get_absolute_edit_url(self):
        return reverse('event-update', args=[self.id])

    def get_absolute_remove_url(self):
        return reverse('event-delete', args=[self.id])
