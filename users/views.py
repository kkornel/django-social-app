import logging

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from djangoapp.settings import EMAIL_FROM_EMAIL

from .admin import User, UserCreationForm
from .decorators import check_recaptcha, prevent_authenticated
from .forms import CaptchaPasswordResetForm, CustomSetPasswordForm
from .tokens import account_activation_token

logger = logging.getLogger(__name__)

# Create your views here.


def home(request):
    return render(request, 'users/home.html')


@prevent_authenticated
@check_recaptcha
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            user = form.save()
            user.send_verification_email(request)
            messages.info(
                request, f'A confirmation email has been sent to {user.email}')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # if user is not None and account_activation_token.check_token(user, token):
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            'Your account has been activated successfully. You are now able to log in.'
        )
        return redirect('login')
    else:
        messages.error(request,
                       'Activation link is invalid!',
                       extra_tags='danger')
        return redirect('login')
        # TODO: might change it later
        # return HttpResponse('Activation link is invalid!')


@check_recaptcha
def reset_password(request):
    if request.method == 'POST':
        form = CaptchaPasswordResetForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            # * Different parameters:
            # form.save(from_email='blabla@blabla.com',
            #           email_template_name='',
            #           html_email_template_name='users/mail_password_reset.html',
            #           request=request,
            #           domain_override="aaaa",
            #           use_https=True,
            #           subject_template_name='users/mail_password_reset_subject.txt')
            form.save(
                request=request,
                from_email=EMAIL_FROM_EMAIL,
                html_email_template_name='users/mail_password_reset.html',
                subject_template_name='users/mail_password_reset_subject.txt')
            return redirect('password_reset_done')
    else:
        form = CaptchaPasswordResetForm()
    return render(request, 'users/password_reset.html', {'form': form})
