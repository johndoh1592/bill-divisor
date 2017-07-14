# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView

from ..models import Event


class StartView(ListView):
    context_object_name = 'events'
    template_name = 'base/start.html'

    def get_queryset(self):
        participants = self.request.user.participant_set
        if participants.exists():
            return Event.objects.filter(event_participants__in=participants.all()).distinct()
        return Event.objects.none()
