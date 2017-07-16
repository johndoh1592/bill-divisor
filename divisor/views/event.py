# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ..models import Event, Participant


class EventCreateView(CreateView):
    model = Event
    fields = ['name', 'start', 'end']
    template_name = 'event/event_create_form.html'

    def form_valid(self, form):
        response = super(EventCreateView, self).form_valid(form)
        Participant.objects.create(
            user=self.request.user,
            event=self.object,
            is_admin=True
        )
        return response


class EventUpdateView(UpdateView):
    model = Event
    template_name = 'event/event_edit_form.html'
    fields = ['name', 'start', 'end']


class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('event-list')


class EventDetailView(DetailView):
    model = Event
    template_name = 'event/event_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)

        if self.object.event_bills.exists():
            active_bills = self.object.event_bills.active_instances()
            inactive_bills = self.object.event_bills.inactive_instances()
            new_event = False
        else:
            new_event = True
            active_bills = []
            inactive_bills = []

        context.update({
            'consuming_groups': self.object.event_consuming_groups.all(),
            'participants': self.object.event_participants.all(),
            'new_event': new_event,
            'active_bills': active_bills,
            'inactive_bills': inactive_bills,
        })
        return context


class EventListView(ListView):
    context_object_name = 'events'
    template_name = 'event/event_list.html'

    def get_queryset(self):
        participants = self.request.user.participant_set
        if participants.exists():
            return Event.objects.filter(event_participants__in=participants.all()).distinct()
        return Event.objects.none()
