# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal, DivisionByZero, InvalidOperation, ROUND_HALF_UP

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


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


class Bill(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    date = models.DateField(verbose_name=_('Date'), default=timezone.now)
    sum_total = models.DecimalField(decimal_places=3, max_digits=16, verbose_name=_('Global positions'),
                                    default=Decimal('0'))
    event = models.ForeignKey('divisor.Event', editable=False, related_name='event_bills')
    is_active = models.BooleanField(default=True)

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
        positions = BillConsumingGroupPosition.objects.filter(bill_id=self.id)
        consuming_group_positions_sum = Decimal('0')

        for position in positions:
            consuming_group_positions_sum += position.value

        self.consuming_groups_positions_sum = consuming_group_positions_sum

        return True


class EventQuerySet(models.QuerySet):
    def active_instances(self):
        return self.filter(is_active=True)

    def inactive_instances(self):
        return self.filter(is_active=False)


class Event(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Name'))
    start = models.DateField(verbose_name=_('Start-date'))
    end = models.DateField(blank=True, null=True, verbose_name=_('End-date'))
    is_active = models.BooleanField(default=True)

    objects = EventQuerySet.as_manager()

    def __unicode__(self):
        return self.get_description()

    def get_name(self):
        return self.name

    def get_description(self):
        return self.get_name() + ' ' + unicode(self.start) + ' - ' + unicode(self.end)

    def get_is_active(self):
        if self.is_active:
            return _('Yes')
        return _('No')

    def get_absolute_detail_url(self):
        return reverse('detail_event', args=[self.id])

    def get_absolute_edit_url(self):
        return reverse('edit_event', args=[self.id])

    def get_absolute_remove_url(self):
        return reverse('remove_event', args=[self.id])
