# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..forms import ConsumingGroupFrom
from ..models import ConsumingGroup, Event, Participant


def create_consuming_group(request, event_id):

    form_action = reverse('create_consuming_group', args=[event_id])
    back_button = reverse('event-detail', kwargs={'pk': event_id})

    if request.method == 'POST':
        consuming_group_form = ConsumingGroupFrom(request.POST, event_id=event_id)
        if consuming_group_form.is_valid():
            consuming_group = ConsumingGroup(
                name=consuming_group_form.cleaned_data['name'],
            )
            consuming_group.event = Event.objects.get(id=event_id)
            consuming_group.save()
            return HttpResponseRedirect(reverse('detail_consuming_group', args=[event_id, consuming_group.id]))
    else:
        consuming_group_form = ConsumingGroupFrom(event_id=event_id)

    context = {
        'consuming_group_form': consuming_group_form,
        'form_action': form_action,
        'back_button': back_button,
    }

    return render(request, 'consuming_group/consuming_group_create_form.html', context)


def edit_consuming_group(request, event_id, consuming_group_id):

    form_action = reverse('edit_consuming_group', args=[event_id, consuming_group_id])
    back_button = reverse('detail_consuming_group', args=[event_id, consuming_group_id])

    consuming_group = ConsumingGroup.objects.get(id=consuming_group_id)

    if request.method == 'POST':
        consuming_group_form = ConsumingGroupFrom(request.POST, instance=consuming_group, event_id=event_id)
        if consuming_group_form.is_valid():
            consuming_group_form.save()
            return HttpResponseRedirect(reverse('detail_consuming_group', args=[event_id, consuming_group_id]))
    else:
        consuming_group_form = ConsumingGroupFrom(instance=consuming_group, event_id=event_id)

    context = {
        'consuming_group_form': consuming_group_form,
        'form_action': form_action,
        'back_button': back_button,
    }

    return render(request, 'consuming_group/consuming_group_edit_form.html', context)


def delete_consuming_group(request, event_id, consuming_group_id):
    consuming_group = ConsumingGroup.objects.get(id=consuming_group_id)
    consuming_group.delete()

    return HttpResponseRedirect(reverse('event-detail', kwargs={'pk': event_id}))


def delete_consuming_group_participant(request, event_id, consuming_group_id):

    response = HttpResponseRedirect(reverse('detail_consuming_group', args=[event_id, consuming_group_id]))

    try:
        sub_group_id = request.GET['sub_group']
        participant_id = request.GET['participant']
    except KeyError:
        return response

    try:
        sub_group_id = int(sub_group_id)
        participant_id = int(participant_id)
    except ValueError:
        return response

    consuming_group = ConsumingGroup.objects.get(id=consuming_group_id)
    participant = Participant.objects.get(id=participant_id)

    if sub_group_id == 25:
        consuming_group.participants_25.remove(participant)
    elif sub_group_id == 50:
        consuming_group.participants_50.remove(participant)
    elif sub_group_id == 75:
        consuming_group.participants_75.remove(participant)
    elif sub_group_id == 100:
        consuming_group.participants_100.remove(participant)

    consuming_group.save()

    return response


def detail_consuming_group(request, event_id, consuming_group_id):

    event = Event.objects.get(id=event_id)
    consuming_group = ConsumingGroup.objects.get(id=consuming_group_id)
    participants_25 = consuming_group.participants_25.all()
    consuming_group_type_25 = {
        'type': 25,
        'name': "25 %"
    }
    participants_50 = consuming_group.participants_50.all()
    consuming_group_type_50 = {
        'type': 50,
        'name': "50 %"
    }
    participants_75 = consuming_group.participants_75.all()
    consuming_group_type_75 = {
        'type': 75,
        'name': "75 %"
    }
    participants_100 = consuming_group.participants_100.all()
    consuming_group_type_100 = {
        'type': 100,
        'name': "100 %"
    }

    context = {
        'event': event,
        'consuming_group': consuming_group,
        'participants_25': participants_25,
        'consuming_group_type_25': consuming_group_type_25,
        'participants_50': participants_50,
        'consuming_group_type_50': consuming_group_type_50,
        'participants_75': participants_75,
        'consuming_group_type_75': consuming_group_type_75,
        'participants_100': participants_100,
        'consuming_group_type_100': consuming_group_type_100,
    }

    return render(request, 'consuming_group/consuming_group_detail.html', context)
