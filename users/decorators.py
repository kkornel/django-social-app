import datetime
import logging
from functools import wraps

import requests
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

logger = logging.getLogger(__name__)


def prevent_authenticated(view_func):
    """
    Custom decorator for preventing logged users from visitng sites
    which are intendent for anonymous users.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            # Begin reCAPTCHA validation
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            r = requests.post(
                'https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            # End reCAPTCHA validation
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request,
                               'Invalid reCAPTCHA. Please try again.',
                               extra_tags='danger')
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def confirm_password(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        last_login = request.user.last_login
        timespan = last_login + datetime.timedelta(seconds=10)
        if timezone.now() > timespan:
            from .views import PasswordConfirmView
            return PasswordConfirmView.as_view()(request, *args, **kwargs)
        return view_func(request, *args, **kwargs)

    return _wrapped_view
