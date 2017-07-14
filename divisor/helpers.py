# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal


def distribute_percent(total, weights=None):
    distributed_total = []
    if not weights:
        weights = (1, 2, 3, 4)
    for weight in weights:
        weight = Decimal(str(weight))
        factor = weight / sum(weights)
        weighted_value = (factor * total)
        distributed_total.append(weighted_value)
    return distributed_total
