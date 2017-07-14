
from django import dispatch

bill_update = dispatch.Signal(providing_args=['bill'])
