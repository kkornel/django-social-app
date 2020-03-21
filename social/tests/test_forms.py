import datetime

from django.test import TestCase
from django.utils import timezone

from social.forms import PostCreateForm


class PostCreateFormTest(TestCase):
    def test_form_content_label(self):
        form = PostCreateForm()

        self.assertTrue(form.fields['content'].label == '')

    def test_form_location_placeholder(self):
        form = PostCreateForm()
        self.assertTrue(form.fields['location'].widget.attrs['placeholder'] ==
                        'Helsinki, Finland')

    def test_form_valid_data(self):
        form = PostCreateForm(
            data={
                'content':
                'Today is the first day of the Spring, it is Saturday 10AM and I am learning how to write tests in Django.',
                'location': 'Tomaszów Mazowiecki'
            })
        self.assertTrue(form.is_valid())

    def test_form_not_valid_data(self):
        form = PostCreateForm(
            data={
                'content':
                'More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters. More than 280 characters.',
                'location': 'More than 40 characters. More than 40 characters.'
            })
        self.assertFalse(form.is_valid())

    def test_form_no_data(self):
        form = PostCreateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
