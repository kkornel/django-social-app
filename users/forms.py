from bootstrap_modal_forms.forms import BSModalForm
from django import forms
from django.contrib.auth.forms import (PasswordChangeForm, PasswordResetForm,
                                       SetPasswordForm)
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from .admin import Profile, User


class CaptchaPasswordResetForm(PasswordResetForm):
    """Custom PasswordResetForm only for styling EmailField."""
    email = forms.EmailField(
        label='',
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': 'Email address'}),
    )


class CustomSetPasswordForm(SetPasswordForm):
    """
    Custom SetPasswordForm only for styling Password fields.
    A form that lets user set password without entering the old one.
    """
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}),
    )
    new_password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'New password confirmation'}),
    )


class CustomChangePasswordForm(PasswordChangeForm):
    """Custom PasswordChangeForm only for styling Password fields."""
    old_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Current password'}),
    )
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}),
    )
    new_password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'New password confirmation'}),
    )


class PasswordConfirmForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': 'Current password'}),
    )

    class Meta:
        model = User
        fields = ('confirm_password', )

    def clean(self):
        cleaned_data = super(PasswordConfirmForm, self).clean()
        confirm_password = cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            self.add_error('confirm_password', 'Password does not match.')

    def save(self, commit=True):
        user = super(PasswordConfirmForm, self).save(commit)
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ()


class UserUpdateFormModal(BSModalForm):
    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateViewModal(BSModalForm):
    bio = forms.CharField(
        required=False,
        max_length=300,
        widget=forms.Textarea(
            attrs={
                'rows': 6,
                'cols': 10,
                #   'style': 'resize:none;',
                'style':
                'resize:none; background-color: #15181c; color: #d9d9d9;',
                'placeholder': 'Tell others a little bit about yourself!',
            }),
    )
    city = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Oslo, Norway',
        }),
    )
    website = forms.CharField(
        required=False,
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'stackoverflow.com',
        }),
    )
    image = forms.ImageField(
        label='Photo',
        required=False,
        widget=forms.FileInput,
    )
    delete_current_image = forms.BooleanField(
        label='Delete current image checkbox:',
        required=False,
    )

    class Meta:
        model = Profile
        fields = ['bio', 'city', 'website', 'image']
