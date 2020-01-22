import logging
from functools import wraps

import requests
from django.conf import settings
from django.contrib import messages

logger = logging.getLogger(__name__)


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

            logger.debug(result)
            logger.debug(result['success'])
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request,
                               'Invalid reCAPTCHA. Please try again.',
                               extra_tags='danger')
        return view_func(request, *args, **kwargs)

    return _wrapped_view
