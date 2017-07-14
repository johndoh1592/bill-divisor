from django.shortcuts import render
from divisor.models import Participant

# Create your views here.
def start(request):

    active_events = []
    inactive_events = []

    if request.user.participant_set.count() > 0:
        participants = request.user.participant_set.all()
        for participant in participants:
            if participant.event.is_active:
                active_events.append(participant.event)
            else:
                inactive_events.append(participant.event)

    context = {
        'active_events': active_events,
        'inactive_events': inactive_events,
    }

    return render(request, 'base/start.html', context)

