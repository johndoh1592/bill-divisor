
from django.dispatch import receiver

from .signals import bill_update
from.models import BillParticipant, BillConsumingGroupPosition

@receiver(bill_update)
def update_bill(sender, **kwargs):

    if sender == BillParticipant:
        bill_participant = sender
