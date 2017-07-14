# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..forms import EventForm
from ..models import Event, Participant


def create_event(request):

    form_action = reverse('create_event')
    back_button = reverse('home')

    if request.method == 'POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            event = Event(
                name=event_form.cleaned_data['name'],
                start=event_form.cleaned_data['start'],
                end=event_form.cleaned_data['end'],
            )
            event.save()
            participant = Participant(
                user=request.user,
                display_name=request.user.username,
                event=event,
                is_admin=True
            )
            participant.save()
            return HttpResponseRedirect(reverse('detail_event', args=[event.id]))
    else:
        event_form = EventForm()

    context = {
        'form_action': form_action,
        'event_form': event_form,
        'back_button': back_button,
    }

    return render(request, 'event/event_create_form.html', context)


def edit_event(request, event_id):

    form_action = reverse('edit_event', args=[event_id])
    back_button = reverse('detail_event', args=[event_id])

    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return HttpResponseRedirect(reverse('detail_event', args=[event_id]))
    else:
        event_form = EventForm(instance=event)

    context = {
        'form_action': form_action,
        'event_form': event_form,
        'back_button': back_button,
    }

    return render(request, 'event/event_edit_form.html', context)


def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()

    return HttpResponseRedirect(reverse('home'))


def detail_event(request, event_id):

    event = Event.objects.get(id=event_id)
    consuming_groups = event.event_consuming_groups.all()
    participants = event.event_participants.all()
    active_bills = event.event_bills.filter(is_active=True)
    inactive_bills = event.event_bills.filter(is_active=False)

    context = {
        'event': event,
        'consuming_groups': consuming_groups,
        'participants': participants,
        'active_bills': active_bills,
        'inactive_bills': inactive_bills,
    }

    return render(request, 'event/event_detail.html', context)
