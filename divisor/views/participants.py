# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..forms import ParticipantForm
from ..models import Event, Participant


def create_participant(request, event_id):

    form_action = reverse('create_participant', args=[event_id])
    back_button = reverse('detail_event', args=[event_id])

    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST, event_id=event_id)
        if participant_form.is_valid():
            participant_form.save()
            return HttpResponseRedirect(reverse('detail_event', args=[event_id]))
    else:
        participant_form = ParticipantForm(event_id=event_id)

    context = {
        'participant_form': participant_form,
        'form_action': form_action,
        'back_button': back_button,
    }

    return render(request, 'participant/participant_create_form.html', context)


def edit_participant(request, event_id, participant_id):

    form_action = reverse('edit_participant', args=[event_id, participant_id])
    back_button = reverse('detail_participant', args=[event_id, participant_id])

    participant = Participant.objects.get(id=participant_id)

    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST, instance=participant, event_id=event_id)
        if participant_form.is_valid():
            participant_form.save()
            return HttpResponseRedirect(reverse('detail_participant', args=[event_id, participant_id]))
    else:
        participant_form = ParticipantForm(instance=participant, event_id=event_id)

    context = {
        'participant_form': participant_form,
        'form_action': form_action,
        'back_button': back_button,
    }

    return render(request, 'participant/participant_edit_form.html', context)


def delete_participant(request, event_id, participant_id):
    participant = Participant.objects.get(id=participant_id)
    participant.delete()

    return HttpResponseRedirect(reverse('detail_event', args=[event_id]))


def detail_participant(request, event_id, participant_id):

    event = Event.objects.get(id=event_id)
    participant = Participant.objects.get(id=participant_id)
    consuming_groups = [
        participant.participant_consuming_group_25_percent,
        participant.participant_consuming_group_50_percent,
        participant.participant_consuming_group_75_percent,
        participant.participant_consuming_group_100_percent,
    ]

    context = {
        'event': event,
        'participant': participant,
        'consuming_groups': consuming_groups,
    }

    return render(request, 'participant/participant_detail.html', context)
