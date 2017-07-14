# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from decimal import Decimal

from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('date', models.DateField(
                    default=datetime.datetime(2015, 8, 23, 16, 3, 31, 579761, tzinfo=utc),
                    verbose_name='Date'
                )),
                ('sum_total', models.DecimalField(
                    default=Decimal('0'),
                    verbose_name='Global positions',
                    max_digits=16,
                    decimal_places=3
                )),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='BillConsumingGroupPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(verbose_name='Value', max_digits=16, decimal_places=3)),
                ('bill', models.ForeignKey(related_name='bill_consuming_positions', editable=False, to='divisor.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='BillParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payed_amount', models.DecimalField(
                    default=Decimal('0'),
                    verbose_name='Payed amount',
                    max_digits=16,
                    decimal_places=3
                )),
                ('own_amount', models.DecimalField(
                    default=Decimal('0'),
                    verbose_name='Own amount',
                    max_digits=16,
                    decimal_places=3
                )),
                ('is_done', models.BooleanField(default=False, editable=False)),
                ('bill', models.ForeignKey(related_name='bill_participants', editable=False, to='divisor.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='ConsumingGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('start', models.DateField(verbose_name='Start-date')),
                ('end', models.DateField(null=True, verbose_name='End-date', blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_name', models.CharField(max_length=255, verbose_name='Display name', blank=True)),
                ('is_admin', models.BooleanField(default=False, editable=False)),
                ('event', models.ForeignKey(related_name='event_participants', to='divisor.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
            },
        ),
        migrations.AddField(
            model_name='consuminggroup',
            name='event',
            field=models.ForeignKey(related_name='event_consuming_groups', editable=False, to='divisor.Event'),
        ),
        migrations.AddField(
            model_name='consuminggroup',
            name='participants_100',
            field=models.ManyToManyField(
                related_name='participant_consuming_group_100_percent',
                verbose_name='100% participants',
                to='divisor.Participant',
                blank=True
            ),
        ),
        migrations.AddField(
            model_name='consuminggroup',
            name='participants_25',
            field=models.ManyToManyField(
                related_name='participant_consuming_group_25_percent',
                verbose_name='25% participants',
                to='divisor.Participant',
                blank=True
            ),
        ),
        migrations.AddField(
            model_name='consuminggroup',
            name='participants_50',
            field=models.ManyToManyField(
                related_name='participant_consuming_group_50_percent',
                verbose_name='50% participants',
                to='divisor.Participant',
                blank=True
            ),
        ),
        migrations.AddField(
            model_name='consuminggroup',
            name='participants_75',
            field=models.ManyToManyField(
                related_name='participant_consuming_group_75_percent',
                verbose_name='75% participants',
                to='divisor.Participant',
                blank=True
            ),
        ),
        migrations.AddField(
            model_name='billparticipant',
            name='participant',
            field=models.ForeignKey(verbose_name='Participant', to='divisor.Participant'),
        ),
        migrations.AddField(
            model_name='billconsuminggroupposition',
            name='consuming_group',
            field=models.ForeignKey(verbose_name='Group', to='divisor.ConsumingGroup'),
        ),
        migrations.AddField(
            model_name='bill',
            name='event',
            field=models.ForeignKey(related_name='event_bills', editable=False, to='divisor.Event'),
        ),
    ]
