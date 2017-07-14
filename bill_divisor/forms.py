# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UsernameField


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'first_name', 'last_name')
        field_classes = {'username': UsernameField}

    def get_user(self, request):
        return authenticate(
            request=request,
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1']
        )
