# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal, DivisionByZero, InvalidOperation, ROUND_HALF_UP

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .queryset import StateQuerySet


class Bill(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    date = models.DateField(verbose_name=_('Date'), default=timezone.now)
    sum_total = models.DecimalField(decimal_places=3, max_digits=16, verbose_name=_('Global positions'),
                                    default=Decimal('0'))
    event = models.ForeignKey('divisor.Event', editable=False, related_name='event_bills')
    is_active = models.BooleanField(default=True)

    objects = StateQuerySet.as_manager()

    @property
    def consuming_groups_positions_sum(self):
        if hasattr(self, 'consuming_group_positions_sum_'):
            return self.consuming_group_positions_sum_
        return Decimal('0')

    @consuming_groups_positions_sum.setter
    def consuming_groups_positions_sum(self, value):
        setattr(self, 'consuming_group_positions_sum_', value)

    @property
    def participants_own_amounts_sum(self):
        participants_own_amounts_sum = Decimal('0')
        for participant in self.bill_participants.all():
            participants_own_amounts_sum += participant.own_amount
        return participants_own_amounts_sum

    @property
    def global_positions(self):
        total_sum = self.sum_total - self.consuming_groups_positions_sum - self.participants_own_amounts_sum
        return total_sum

    @property
    def partial_global_value(self):
        try:
            p_value = self.global_positions / self.bill_participants.count()
            p_value = p_value.quantize(Decimal('.000'), rounding=ROUND_HALF_UP)
        except (InvalidOperation, DivisionByZero):
            p_value = Decimal('0')
        return p_value

    def __init__(self, *args, **kwargs):
        super(Bill, self).__init__(*args, **kwargs)
        if self.id:
            self.sum_consuming_group_positions()

    def __unicode__(self):
        return self.get_description()

    def get_name(self):
        return self.name

    def get_description(self):
        return self.get_name() + ' ' + unicode(self.date)

    def get_is_active(self):
        if self.is_active:
            return _('Yes')
        return _('No')

    def get_absolute_detail_url(self):
        return reverse('detail_bill', args=[self.event_id, self.id])

    def get_absolute_edit_url(self):
        return reverse('edit_bill', args=[self.event_id, self.id])

    def get_absolute_remove_url(self):
        return reverse('remove_bill', args=[self.event_id, self.id])

    def sum_consuming_group_positions(self):
        positions = self.bill_consuming_positions.all()
        consuming_group_positions_sum = Decimal('0')

        for position in positions:
            consuming_group_positions_sum += position.value

        self.consuming_groups_positions_sum = consuming_group_positions_sum

        return True
