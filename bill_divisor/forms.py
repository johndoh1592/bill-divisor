# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _


def user_credentials(username, password):
    """
    Provides the credentials required to authenticate the user for login.
    :param password: unicode
    :param username: unicode
    """

    credentials = {
        "username": username,
        "password": password
    }

    return credentials


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_('Username'),
        max_length=30,
        required=True,
        error_messages={'required': _('Please enter your desired username.')},
    )

    password = forms.CharField(
        label=_('Password'),
        required=True,
        widget=forms.PasswordInput(render_value=False),
        error_messages={'required': _('Please enter a password.')},
    )

    user = None

    def clean(self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            try:
                credentials = user_credentials(self.cleaned_data['username'], self.cleaned_data['password'])
                self.user = authenticate(**credentials)
            except ObjectDoesNotExist:
                raise forms.ValidationError(_('The Username and/or password are not correct'))
        return self.cleaned_data

    def login(self, request):
        if self.is_valid():
            login(request, self.user)


class RegisterForm(forms.Form):
    username = forms.CharField(
        label=_('Username'),
        max_length=30,
        error_messages={'required': _('Please enter your desired username.')},
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(render_value=False),
        error_messages={'required': _('Please enter a password.')},
    )

    password_check = forms.CharField(
        label=_('Retype your Password'),
        widget=forms.PasswordInput(render_value=False),
        error_messages={'required': _('Please enter a password.')},
    )

    email = forms.EmailField(
        label=_('Email'),
        required=False
    )

    def clean_username(self):

        if not re.search(r'^[\w.@+-]+$', self.cleaned_data['username']):
            raise forms.ValidationError(_('Enter a valid username. This value may contain only letters, numbers and '
                                          '@/./+/-/_ characters.'))
        try:
            User.objects.get(username=self.cleaned_data['username'])
            raise forms.ValidationError(_('This username already exists, please login or choose another one'))
        except ObjectDoesNotExist:
            pass

        return self.cleaned_data['username']

    def clean_password_check(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_check']:
            raise forms.ValidationError(_('Passwords don\'t match '))

    def save(self, request):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['password'])
        user.save()

        credentials = user_credentials(self.cleaned_data['username'], self.cleaned_data['password'])

        authenticated_user = authenticate(**credentials)

        login(request, authenticated_user)
