import datetime

from django.test import TestCase
from django.utils import timezone

from users.admin import UserCreationForm
from users.models import User


class UserCreationFormTest(TestCase):
    def test_form_username_label(self):
        form = UserCreationForm()
        self.assertTrue(form.fields['username'].label == '')

    def test_form_username_widget_class(self):
        form = UserCreationForm()
        self.assertTrue(form.fields['email'].widget.attrs['placeholder'] ==
                        'Email address')

    def test_form_valid_data(self):
        form = UserCreationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'testuser',
                'password1': 'TempraryPass123!',
                'password2': 'TempraryPass123!',
            })
        self.assertTrue(form.is_valid())

    def test_form_not_valid_email(self):
        user = User.objects.create(email='user@gmail.com', username='user')
        password = 'temporary'
        user.set_password(password)
        user.is_active = True
        user.save()

        form = UserCreationForm(
            data={
                'email': 'user@gmail.com',
                'username': 'user1',
                'password1': 'TempraryPass123!',
                'password2': 'TempraryPass123!',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': 'testuser@gmail',
                'username': 'testuser',
                'password1': 'TempraryPass123!',
                'password2': 'TempraryPass123!',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': 'testusergmail.com',
                'username': 'testuser',
                'password1': 'TempraryPass123!',
                'password2': 'TempraryPass123!',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': '@gmail',
                'username': 'testuser',
                'password1': 'TempraryPass123!',
                'password2': 'TempraryPass123!',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': 'testuser@',
                'username': 'testuser',
                'password1': 'TempraryPass123!',
                'password2': 'TempraryPass123!',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': '@gmail.com',
                'username': 'testuser',
                'password1': 'TempraryPass123!',
                'password2': 'TempraryPass123!',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': '',
                'username': 'testuser',
                'password1': 'TempraryPass123!',
                'password2': 'TempraryPass123!',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_form_not_valid_username(self):
        user1 = User.objects.create(email='user1@mail.com', username='user1')
        password = 'temporary'
        user1.set_password(password)
        user1.is_active = True
        user1.save()

        form = UserCreationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user1',
                'password1': 'TempraryPass123!',
                'password2': 'TempraryPass123!',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': '',
                'password1': 'TempraryPass123!',
                'password2': 'TempraryPass123!',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'MORETHAN20MORETHAN20MORETHAN20MORETHAN20',
                'password1': 'TempraryPass123!',
                'password2': 'TempraryPass123!',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_form_not_valid_password(self):
        form = UserCreationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user1',
                'password1': '',
                'password2': 'TempraryPass123!',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user1',
                'password1': 'TempraryPass123!',
                'password2': '',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user1',
                'password1': 'Match',
                'password2': 'NoMatchNoMatch',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user1',
                'password1': '1234',
                'password2': '1234',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

        form = UserCreationForm(
            data={
                'email': 'testuser@gmail.com',
                'username': 'user1',
                'password1': 'test123',
                'password2': 'test123',
            })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_form_no_data(self):
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
