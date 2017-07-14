# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView as DjangoLoginView, SuccessURLAllowedHostsMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import CreateView

from .forms import RegisterForm


# noinspection PyClassHasNoInit
class LoginView(DjangoLoginView):
    template_name = 'base/login.html'


class RegisterView(SuccessURLAllowedHostsMixin, CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('home')
    template_name = 'base/register.html'

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(RegisterView, self).form_valid(form)
        auth_login(self.request, form.get_user(self.request))
        return response
