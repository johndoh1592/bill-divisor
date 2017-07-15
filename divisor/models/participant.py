# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class Participant(models.Model):
    user = models.ForeignKey('auth.User')
    display_name = models.CharField(max_length=255, blank=True, verbose_name=_('Display name'))
    event = models.ForeignKey('divisor.Event', related_name='event_participants')
    is_admin = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')
        unique_together = ('user', 'event')

    def __unicode__(self):
        return self.get_name()

    def get_name(self):
        if self.display_name != '':
            return self.display_name
        return self.user.username

    def get_description(self):
        return self.get_name()

    def get_absolute_detail_url(self):
        return reverse('detail_participant', args=[self.event_id, self.id])

    def get_absolute_edit_url(self):
        return reverse('edit_participant', args=[self.event_id, self.id])

    def get_absolute_remove_url(self):
        return reverse('remove_participant', args=[self.event_id, self.id])


class BillParticipant(models.Model):
    participant = models.ForeignKey('divisor.Participant', verbose_name=_('Participant'))
    bill = models.ForeignKey('divisor.Bill', editable=False, related_name='bill_participants')
    payed_amount = models.DecimalField(decimal_places=3, max_digits=16, verbose_name=_('Payed amount'),
                                       default=Decimal('0'))
    own_amount = models.DecimalField(decimal_places=3, max_digits=16, verbose_name=_('Own amount'),
                                     default=Decimal('0'))
    is_done = models.BooleanField(default=False, editable=False)

    @property
    def payable_amount(self):
        sum_payable = Decimal('0')
        sum_payable += self.bill.partial_global_value
        sum_payable += self.own_amount
        for position in self.bill.bill_consuming_positions.all():
            member = position.consuming_group.is_member(self)
            if member:
                sum_payable += position.position_values[member]
        sum_payable -= self.payed_amount

        return sum_payable

    @property
    def final_payed_amount(self):
        if hasattr(self, 'final_payed_amount_'):
            return self.final_payed_amount_

        return self.payed_amount

    @final_payed_amount.setter
    def final_payed_amount(self, amount):
        value = self.final_payed_amount + amount
        setattr(self, 'final_payed_amount_', value)

    @property
    def final_payable_amount(self):
        if hasattr(self, 'final_payable_amount_'):
            return self.final_payable_amount_

        return self.payable_amount

    @final_payable_amount.setter
    def final_payable_amount(self, amount):
        value = self.final_payable_amount - amount
        setattr(self, 'final_payable_amount_', value)

    def __unicode__(self):
        return self.get_description()

    def get_name(self):
        try:
            name = self.participant.user.username
        except AttributeError:
            name = ''
        return name

    def get_description(self):
        return _('{name} has to pay: {payable_amount} | has payed: {payed_amount}').format(
            name=self.get_name(),
            payable_amount=self.payable_amount,
            payed_amount=self.payed_amount
        )

    def get_is_done(self):
        if self.is_done:
            return _('Yes')
        return _('No')

    def get_absolute_detail_url(self):
        return reverse('detail_bill_participant', args=[self.bill.event_id, self.bill_id, self.id])

    def get_absolute_edit_url(self):
        return reverse('edit_bill_participant', args=[self.bill.event_id, self.bill_id, self.id])

    def get_absolute_remove_url(self):
        return reverse('remove_bill_participant', args=[self.bill.event_id, self.bill_id, self.id])
