import logging

from bootstrap_modal_forms.generic import BSModalUpdateView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import ListView, UpdateView

from djangoapp.settings import EMAIL_FROM_EMAIL
from social.models import Post, Profile
from users import forms as user_forms

from .admin import User, UserCreationForm
from .decorators import (check_recaptcha, confirm_password,
                         prevent_authenticated)
from .tokens import account_activation_token

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'social/home.html')


@prevent_authenticated
@check_recaptcha
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            user = form.save()
            user.send_verification_email(request)
            # TODO remove later
            user.is_active = True
            user.save()
            messages.info(
                request, f'A confirmation email has been sent to {user.email}')
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {
        'title': 'Sign Up!',
        'form': form,
    }

    return render(request, 'users/register.html', context)


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            'Your account has been activated successfully. You are now able to log in.'
        )
        return redirect('login')
    else:
        messages.error(
            request,
            'Activation link is invalid!',
            extra_tags='danger',
        )
        return redirect('login')


@check_recaptcha
def reset_password(request):
    if request.method == 'POST':
        form = user_forms.CaptchaPasswordResetForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            # * Different parameters:
            # form.save(from_email='blabla@blabla.com',
            #           email_template_name='',
            #           html_email_template_name='users/mail_password_reset.html',
            #           request=request,
            #           domain_override='aaaa',
            #           use_https=True,
            #           subject_template_name='users/mail_password_reset_subject.txt')
            form.save(
                request=request,
                from_email=EMAIL_FROM_EMAIL,
                html_email_template_name='users/mail_password_reset.html',
                subject_template_name='users/mail_password_reset_subject.txt',
            )
            return redirect('password_reset_done')
    else:
        form = user_forms.CaptchaPasswordResetForm()

    context = {
        'title': 'Password reset',
        'form': form,
    }

    return render(request, 'users/password_reset.html', context)


class PasswordConfirmView(UpdateView):
    form_class = user_forms.PasswordConfirmForm
    template_name = 'users/password_confirm.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Confirm password'
        return context

    def get_success_url(self):
        return self.request.get_full_path()


@login_required
@check_recaptcha
def password_change(request):
    if request.method == 'POST':
        form = user_forms.CustomChangePasswordForm(
            data=request.POST,
            user=request.user,
        )
        if form.is_valid() and request.recaptcha_is_valid:
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed.')
            return redirect('profile', username=request.user.username)
    else:
        form = user_forms.CustomChangePasswordForm(user=request.user)

    context = {
        'title': 'Password change',
        'form': form,
    }

    return render(request, 'users/password_change.html', context)


def is_user_owner_of_the_account(user, request):
    test = user == request.user
    return test


def delete_user(request, user):
    user.delete()
    messages.success(request, 'Your account has been deleted.')
    logger.debug('Account has been deleted.')
    return redirect('login')


@login_required
@confirm_password
def delete_account(request, username):
    form = user_forms.UserDeleteForm
    try:
        user = User.objects.get(username=username)
        user_passes_test = is_user_owner_of_the_account(user, request)
        if not user_passes_test:
            return HttpResponseForbidden()
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('profile', username=request.user.username)
    except Exception as e:
        messages.error(request, e.message)
        return redirect('profile', username=request.user.username)

    if request.method == 'POST':
        delete_user(request, user)
        return redirect('login')

    context = {
        'title': 'Delete account',
        'form': form,
        'myuser': request.user,
    }

    return render(request, 'users/account_delete_confirm.html', context)


class ProfileDetailListView(LoginRequiredMixin, ListView):
    """https://stackoverflow.com/questions/41287431/django-combine-detailview-and-listview"""
    detail_context_object_name = 'profile'
    model = Post
    template_name = 'users/profile.html'
    context_object_name = 'posts'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProfileDetailListView, self).get(request, *args, **kwargs)

    def get_object(self):
        username = self.kwargs.get('username')
        user = User.objects.get(username=username)
        return get_object_or_404(Profile, user=user)

    def get_queryset(self):
        return Post.objects.filter(author=self.object).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailListView, self).get_context_data(**kwargs)
        context[self.detail_context_object_name] = self.object
        context['title'] = f'{self.get_object().user.username}'
        return context


class UserUpdateViewModal(UserPassesTestMixin, BSModalUpdateView):
    model = User
    template_name = 'users/profile_edit_modal.html'
    form_class = user_forms.UserUpdateFormModal
    # success_message = 'Email successfully changed.'
    # success_url = '/profile'
    success_message = ''

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def test_func(self):
        user = self.get_object()
        return self.request.user == user


class ProfileUpdateViewModal(UserPassesTestMixin, BSModalUpdateView):
    model = Profile
    template_name = 'users/profile_edit_modal.html'
    form_class = user_forms.ProfileUpdateViewModal
    # success_message = 'Profile successfully updated.'
    # success_url = '/profile'
    success_message = ''

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def form_valid(self, form):
        profile = self.request.user.profile
        delete_current_image = form.cleaned_data['delete_current_image']

        image_from_profile = profile.image
        image_from_form = form.cleaned_data['image']

        uploaded_new_image = image_from_form != image_from_profile

        if delete_current_image and not uploaded_new_image:
            form.instance.image.delete(save=False)

        if uploaded_new_image:
            # Update and delete
            # I have to delete current image,
            # but the image will be updated by saving form,
            # so it is not on me to do.
            profile.delete_image()

        return super().form_valid(form)

    def test_func(self):
        """
        This function is run by UserPassesTestMixin to check something that we want to check.
        In this case we want to check if the currently logged in user is also the author of the post.
        If he is not, then he has no permissions to do that.
        """
        profile = self.get_object()
        return self.request.user.profile == profile


# Used this to have two forms in one view.
# Firstly I had a templte using this view,
# but I went with modals, so not using it currently.
# Leaving for future.

# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         myuser_form = MyUserUpdateForm(request.POST, instance=request.user)
#         profile_form = ProfileUpdateForm(request.POST,
#                                              request.FILES,
#                                              instance=request.user.profile)

#         if myuser_form.is_valid() and profile_form.is_valid():
#             # TODO delete img.
#             # TODO update with solution from CBS from above
#             delete_current_image = profile_form.cleaned_data[
#                 'delete_current_image']
#             logger.debug(delete_current_image)
#             if delete_current_image:
#                 profile = request.user.profile
#                 current_image = profile.image
#                 if current_image.name != 'default.jpg':
#                     logger.debug('current_image.name != 'default.jpg'')
#                     profile.image.delete(save=False)
#                     logger.debug('deleted old')
#                     new = storage.open('default.jpg').read()
#                     logger.debug(new)
#                     logger.debug(type(new))
#                     filee = File(new)
#                     logger.debug(filee)
#                     logger.debug(type(filee))
#                     # profile.image.save('default.jpg', filee)
#                     logger.debug('lil')
#             myuser_form.save()
#             profile_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('profile')

#     else:
#         myuser_form = MyUserUpdateForm(instance=request.user)
#         profile_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         'myuser_form': myuser_form,
#         'profile_form': profile_form,
#     }

#     return render(request, 'users/profile_edit_modal.html', context)
