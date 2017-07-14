import re
from copy import deepcopy

from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Event, Participant, ConsumingGroup, Bill, BillConsumingGroupPosition, BillParticipant


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'start', 'end']


class ParticipantForm(forms.Form):

    event = None
    user = None

    username = forms.CharField(
        label=_(u'Username'),
        max_length=30,
        error_messages={'required': _(u'Please enter your desired username.')},
    )

    password = forms.CharField(
        label=_(u'Password'),
        widget=forms.PasswordInput(render_value=False),
        error_messages={'required': _(u'Please enter a password.')},
    )

    password_check = forms.CharField(
        label=_(u'Password'),
        widget=forms.PasswordInput(render_value=False),
        error_messages={'required': _(u'Please enter a password.')},
    )

    display_name = forms.CharField(
        label=_(u'Display name'),
        max_length=255,
        required=False,
    )

    email = forms.EmailField(
        label=_(u'Email'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id')
        instance = kwargs.pop('instance', None)
        self.event = Event.objects.get(id=event_id)
        if instance:
            self.base_fields['username'].initial = instance.user.username
            self.base_fields['password'].initial = instance.user.password
            self.base_fields['password_check'].initial = instance.user.password
            self.base_fields['display_name'].initial = instance.display_name
            self.base_fields['email'].initial = instance.user.email
        super(ParticipantForm, self).__init__(*args, **kwargs)

    def clean_username(self):

        if not re.search(r'^[\w.@+-]+$', self.cleaned_data['username']):
            raise forms.ValidationError(_(u'Enter a valid username. This value may contain only letters, numbers and @/'
                                          u'./+/-/_ characters.'))
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
            raise forms.ValidationError(_(u'This username already exists, please login or choose another one'))
        except ObjectDoesNotExist:
            pass

        return self.cleaned_data['username']

    def clean_password_check(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_check']:
            raise forms.ValidationError(_(u'Passwords don\'t match '))

    def save(self):
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
        except ObjectDoesNotExist:
            user = None

        if user:

            user.username = self.cleaned_data['username']
            user.set_password(self.cleaned_data['password'])
            user.email = self.cleaned_data['email']
            user.save()

            try:
                participant = Participant.objects.get(user_id=user.id)
            except ObjectDoesNotExist:
                participant = None

            if participant:
                participant.display_name = self.cleaned_data['display_name']
            else:
                participant = Participant(
                    user=user,
                    display_name=self.cleaned_data['display_name'],
                    event=self.event
                )
        else:
            user = User(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email']
            )
            user.set_password(self.cleaned_data['password'])
            user.save()

            participant = Participant(
                user=user,
                display_name=self.cleaned_data['display_name'],
                event=self.event
            )

        self.user = user

        participant.save()


class ConsumingGroupFrom(forms.ModelForm):

    class Meta:
        model = ConsumingGroup
        fields = ['name', 'participants_25', 'participants_50', 'participants_75', 'participants_100']

    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id')
        super(ConsumingGroupFrom, self).__init__(*args, **kwargs)
        query_set = Participant.objects.filter(event_id=event_id)
        self.fields['participants_25'].queryset = query_set
        self.fields['participants_50'].queryset = query_set
        self.fields['participants_75'].queryset = query_set
        self.fields['participants_100'].queryset = query_set

    def clean_participants_25(self):

        for participant in self.cleaned_data.get('participants_25', []):
            if participant in self.cleaned_data.get('participants_50', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 50%'))
            if participant in self.cleaned_data.get('participants_75', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 75%'))
            if participant in self.cleaned_data.get('participants_100', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 100%'))

        return self.cleaned_data['participants_25']

    def clean_participants_50(self):

        for participant in self.cleaned_data.get('participants_50', []):
            if participant in self.cleaned_data.get('participants_25', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 25%'))
            if participant in self.cleaned_data.get('participants_75', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 75%'))
            if participant in self.cleaned_data.get('participants_100', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 100%'))

        return self.cleaned_data['participants_50']

    def clean_participants_75(self):

        for participant in self.cleaned_data.get('participants_75', []):
            if participant in self.cleaned_data.get('participants_25', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 25%'))
            if participant in self.cleaned_data.get('participants_50', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 50%'))
            if participant in self.cleaned_data.get('participants_100', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 100%'))

        return self.cleaned_data['participants_75']

    def clean_participants_100(self):

        for participant in self.cleaned_data.get('participants_100', []):
            if participant in self.cleaned_data.get('participants_25', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 25%'))
            if participant in self.cleaned_data.get('participants_50', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 50%'))
            if participant in self.cleaned_data.get('participants_75', []):
                raise forms.ValidationError(participant.get_name() + u' ' + _(u'is also in participants 75%'))

        return self.cleaned_data['participants_100']


class BillForm(forms.ModelForm):

    class Meta:
        model = Bill
        fields = ['name', 'date', 'sum_total']


class BillParticipantForm(forms.ModelForm):

    class Meta:
        model = BillParticipant
        fields = ['participant', 'payed_amount', 'own_amount']

    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id')
        super(BillParticipantForm, self).__init__(*args, **kwargs)
        choices = Participant.objects.filter(event_id=event_id)
        self.fields['participant'].queryset = choices


class BillPositionForm(forms.ModelForm):

    class Meta:
        model = BillConsumingGroupPosition
        fields = ['value', 'consuming_group']

    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id')
        super(BillPositionForm, self).__init__(*args, **kwargs)
        choices = ConsumingGroup.objects.filter(event_id=event_id)
        self.fields['consuming_group'].queryset = choices
