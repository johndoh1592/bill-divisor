# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import logout as user_logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, RegisterForm


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('start'))

    return HttpResponseRedirect(reverse('login'))


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_form.login(request)
            return HttpResponseRedirect(reverse('start'))
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'base/login.html', context)


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save(request)
            return HttpResponseRedirect(reverse('start'))
    else:
        register_form = RegisterForm()
    context = {
        'register_form': register_form,
    }
    return render(request, 'base/register.html', context)


def logout(request):
    user_logout(request)

    return HttpResponseRedirect(reverse('home'))
