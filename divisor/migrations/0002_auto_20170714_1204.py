# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.utils.timezone

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divisor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date'),
        ),
    ]
