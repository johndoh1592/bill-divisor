# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal, DivisionByZero, InvalidOperation, ROUND_HALF_UP

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class ConsumingGroup(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Name'))
    event = models.ForeignKey('divisor.Event', editable=False, related_name='event_consuming_groups')
    participants_25 = models.ManyToManyField('divisor.Participant', blank=True, verbose_name=_('25% participants'),
                                             related_name='participant_consuming_group_25_percent')
    participants_50 = models.ManyToManyField('divisor.Participant', blank=True, verbose_name=_('50% participants'),
                                             related_name='participant_consuming_group_50_percent')
    participants_75 = models.ManyToManyField('divisor.Participant', blank=True, verbose_name=_('75% participants'),
                                             related_name='participant_consuming_group_75_percent')
    participants_100 = models.ManyToManyField('divisor.Participant', blank=True, verbose_name=_('100% participants'),
                                              related_name='participant_consuming_group_100_percent')

    @property
    def participant_count(self):
        return (
            self.participants_25.count() +
            self.participants_50.count() +
            self.participants_75.count() +
            self.participants_100.count()
        )

    def __unicode__(self):
        return self.get_name()

    def get_name(self):
        return self.name

    def get_description(self):
        return self.get_name()

    def get_absolute_detail_url(self):
        return reverse('detail_consuming_group', args=[self.event_id, self.id])

    def get_absolute_edit_url(self):
        return reverse('edit_consuming_group', args=[self.event_id, self.id])

    def get_absolute_remove_url(self):
        return reverse('remove_consuming_group', args=[self.event_id, self.id])

    def get_absolute_remove_participant_from_consuming_group_url(self):
        return reverse('remove_consuming_group_participant', args=[self.event_id, self.id])

    def get_values(self, value):

        meta_count = (
            self.participants_25.count() +
            (2 * self.participants_50.count()) +
            (3 * self.participants_75.count()) +
            (4 * self.participants_100.count())
        )

        try:
            meta_partial_value = Decimal(value / meta_count).quantize(Decimal('.000'), rounding=ROUND_HALF_UP)
        except (DivisionByZero, InvalidOperation):
            meta_partial_value = Decimal('0')

        value_25 = meta_partial_value
        value_50 = 2 * meta_partial_value
        value_75 = 3 * meta_partial_value
        value_100 = 4 * meta_partial_value

        values = {
            'value_25': value_25,
            'value_50': value_50,
            'value_75': value_75,
            'value_100': value_100,
        }

        return values

    def is_member(self, participant):
        if self.participants_25.filter(id=participant.participant_id).count() > 0:
            return 'value_25'
        elif self.participants_50.all().filter(id=participant.participant_id).count() > 0:
            return 'value_50'
        elif self.participants_75.filter(id=participant.participant_id).count() > 0:
            return 'value_50'
        elif self.participants_100.filter(id=participant.participant_id).count() > 0:
            return 'value_100'
        return False


class BillConsumingGroupPosition(models.Model):
    bill = models.ForeignKey('divisor.Bill', editable=False, related_name='bill_consuming_positions')
    value = models.DecimalField(decimal_places=3, max_digits=16, verbose_name=_('Value'))
    consuming_group = models.ForeignKey('divisor.ConsumingGroup', verbose_name=_('Group'))

    @property
    def position_values(self):
        if hasattr(self, 'position_values_'):
            return self.position_values_
        return Decimal('0')

    @position_values.setter
    def position_values(self, value):
        setattr(self, 'position_values_', value)

    @property
    def partial_value_25(self):
        return self.position_values['value_25']

    @property
    def partial_value_50(self):
        return self.position_values['value_50']

    @property
    def partial_value_75(self):
        return self.position_values['value_75']

    @property
    def partial_value_100(self):
        return self.position_values['value_100']

    def __init__(self, *args, **kwargs):
        super(BillConsumingGroupPosition, self).__init__(*args, **kwargs)
        if self.id:
            self.position_values = self.consuming_group.get_values(self.value)

    def __unicode__(self):
        return self.get_description()

    def get_name(self):
        try:
            name = self.consuming_group.name
        except AttributeError:
            name = ''
        return name

    def get_description(self):
        return self.get_name() + ' ' + _('value') + ': ' + unicode(self.value)

    def get_absolute_detail_url(self):
        return reverse('detail_bill_position', args=[self.bill.event_id, self.bill_id, self.id])

    def get_absolute_edit_url(self):
        return reverse('edit_bill_position', args=[self.bill.event_id, self.bill_id, self.id])

    def get_absolute_remove_url(self):
        return reverse('remove_bill_position', args=[self.bill.event_id, self.bill_id, self.id])