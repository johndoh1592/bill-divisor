# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..forms import BillForm, BillParticipantForm, BillPositionForm
from ..models import Bill, BillConsumingGroupPosition, BillParticipant, Event


def create_bill(request, event_id):

    form_action = reverse('create_bill', args=[event_id])
    back_button = reverse('event-detail', kwargs={'pk': event_id})

    if request.method == 'POST':
        bill_form = BillForm(request.POST)
        if bill_form.is_valid():
            bill = Bill(
                name=bill_form.cleaned_data['name'],
                date=bill_form.cleaned_data['date'],
            )
            bill.event = Event.objects.get(id=event_id)
            bill.save()

            return HttpResponseRedirect(reverse('detail_bill', args=[event_id, bill.id]))
    else:
        bill_form = BillForm()

    context = {
        'bill_form': bill_form,
        'form_action': form_action,
        'back_button': back_button,
    }

    return render(request, 'bill/bill_create_form.html', context)


def edit_bill(request, event_id, bill_id):

    form_action = reverse('edit_bill', args=[event_id, bill_id])
    back_button = reverse('detail_bill', args=[event_id, bill_id])

    bill = Bill.objects.get(id=bill_id)

    if request.method == 'POST':
        bill_form = BillForm(request.POST, instance=bill)
        if bill_form.is_valid():
            bill_form.save()
            return HttpResponseRedirect(reverse('detail_bill', args=[event_id, bill_id]))
    else:
        bill_form = BillForm(instance=bill)

    context = {
        'bill_form': bill_form,
        'form_action': form_action,
        'back_button': back_button,
    }

    return render(request, 'bill/bill_edit_form.html', context)


def delete_bill(request, event_id, bill_id):
    bill = Bill.objects.get(id=bill_id)
    bill.delete()

    return HttpResponseRedirect(reverse('event-detail', kwargs={'pk': event_id}))


def detail_bill(request, event_id, bill_id):

    event = Event.objects.get(id=event_id)
    bill = Bill.objects.get(id=bill_id)
    bill_participants = bill.bill_participants.all()
    bill_positions = bill.bill_consuming_positions.all()

    context = {
        'event': event,
        'bill': bill,
        'bill_participants': bill_participants,
        'bill_positions': bill_positions
    }

    return render(request, 'bill/bill_detail.html', context)


def create_bill_participant(request, event_id, bill_id):

    form_action = reverse('create_bill_participant', args=[event_id, bill_id])
    back_button = reverse('detail_bill', args=[event_id, bill_id])

    if request.method == 'POST':
        bill_participant_form = BillParticipantForm(request.POST, event_id=event_id)
        if bill_participant_form.is_valid():
            bill_participant = BillParticipant(
                participant=bill_participant_form.cleaned_data['participant'],
                payed_amount=bill_participant_form.cleaned_data['payed_amount'],
                own_amount=bill_participant_form.cleaned_data['own_amount'],
            )
            bill_participant.bill = Bill.objects.get(id=bill_id)
            bill_participant.save()
            return HttpResponseRedirect(
                reverse('detail_bill_participant', args=[event_id, bill_id, bill_participant.id])
            )
    else:
        bill_participant_form = BillParticipantForm(event_id=event_id)

    context = {
        'bill_participant_form': bill_participant_form,
        'form_action': form_action,
        'back_button': back_button,
    }

    return render(request, 'bill/bill_participant_create_form.html', context)


def edit_bill_participant(request, event_id, bill_id, bill_participant_id):

    form_action = reverse('edit_bill_participant', args=[event_id, bill_id, bill_participant_id])
    back_button = reverse('detail_bill_participant', args=[event_id, bill_id, bill_participant_id])

    bill_participant = BillParticipant.objects.get(id=bill_participant_id)

    if request.method == 'POST':
        bill_participant_form = BillParticipantForm(request.POST, instance=bill_participant, event_id=event_id)
        if bill_participant_form.is_valid():
            bill_participant_form.save()
            return HttpResponseRedirect(
                reverse('detail_bill_participant', args=[event_id, bill_id, bill_participant_id])
            )
    else:
        bill_participant_form = BillParticipantForm(instance=bill_participant, event_id=event_id)

    context = {
        'bill_participant_form': bill_participant_form,
        'form_action': form_action,
        'back_button': back_button,
    }

    return render(request, 'bill/bill_participant_edit_form.html', context)


def delete_bill_participant(request, event_id, bill_id, bill_participant_id):
    bill_participant = BillParticipant.objects.get(id=bill_participant_id)
    bill_participant.delete()

    return HttpResponseRedirect(reverse('detail_bill', args=[event_id, bill_id]))


def detail_bill_participant(request, event_id, bill_id, bill_participant_id):

    event = Event.objects.get(id=event_id)
    bill = Bill.objects.get(id=bill_id)
    bill_participant = BillParticipant.objects.get(id=bill_participant_id)

    context = {
        'event': event,
        'bill': bill,
        'bill_participant': bill_participant,
    }

    return render(request, 'bill/bill_participant_detail.html', context)


def create_bill_position(request, event_id, bill_id):

    form_action = reverse('create_bill_position', args=[event_id, bill_id])
    back_button = reverse('detail_bill', args=[event_id, bill_id])

    if request.method == 'POST':
        bill_position_form = BillPositionForm(request.POST, event_id=event_id)
        if bill_position_form.is_valid():
            bill_position = BillConsumingGroupPosition(
                value=bill_position_form.cleaned_data['value'],
                consuming_group=bill_position_form.cleaned_data['consuming_group'],
            )
            bill_position.bill = Bill.objects.get(id=bill_id)
            bill_position.save()
            return HttpResponseRedirect(reverse('detail_bill_position', args=[event_id, bill_id, bill_position.id]))
    else:
        bill_position_form = BillPositionForm(event_id=event_id)

    context = {
        'bill_position_form': bill_position_form,
        'form_action': form_action,
        'back_button': back_button,
    }

    return render(request, 'bill/bill_position_create_form.html', context)


def edit_bill_position(request, event_id, bill_id, bill_position_id):

    form_action = reverse('edit_bill_position', args=[event_id, bill_id, bill_position_id])
    back_button = reverse('detail_bill_position', args=[event_id, bill_id, bill_position_id])

    bill_position = BillConsumingGroupPosition.objects.get(id=bill_position_id)

    if request.method == 'POST':
        bill_position_form = BillPositionForm(request.POST, instance=bill_position, event_id=event_id)
        if bill_position.is_valid():
            bill_position_form.save()
            return HttpResponseRedirect(reverse('detail_bill_position', args=[event_id, bill_id, bill_position_id]))
    else:
        bill_position_form = BillPositionForm(instance=bill_position, event_id=event_id)

    context = {
        'bill_position_form': bill_position_form,
        'form_action': form_action,
        'back_button': back_button,
    }

    return render(request, 'bill/bill_position_edit_form.html', context)


def delete_bill_position(request, event_id, bill_id, bill_position_id):
    bill_position = BillConsumingGroupPosition.objects.get(id=bill_position_id)
    bill_position.delete()

    return HttpResponseRedirect(reverse('detail_bill', args=[event_id, bill_id]))


def detail_bill_position(request, event_id, bill_id, bill_position_id):

    event = Event.objects.get(id=event_id)
    bill = Bill.objects.get(id=bill_id)
    bill_position = BillConsumingGroupPosition.objects.get(id=bill_position_id)

    context = {
        'event': event,
        'bill': bill,
        'bill_position': bill_position
    }

    return render(request, 'bill/bill_position_detail.html', context)
