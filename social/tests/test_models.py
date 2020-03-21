from django.test import TestCase
from django.utils import timezone

from social.models import Post
from users.models import Profile, User


class PostTestModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        cls.user = User.objects.create(email='kornel@mail.com',
                                       username='kornel1')
        cls.profile = cls.user.profile
        cls.profile.bio = 'Northen man'
        cls.profile.city = 'Stockholm'
        cls.profile.website = 'facebook.com'

        cls.post = Post.objects.create(
            author=cls.profile,
            content='Learning tests in Django Framework',
            date_posted=timezone.now(),
            location='Tomaszów Mazowiecki')

    def setUp(self):
        """setUp: Run once for every test method to setup clean data."""
        pass

    def test_content_label(self):
        field_label = self.post._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'content')
        self.assertNotEquals(field_label, 'location')

    def test_location_max_length(self):
        max_length = self.post._meta.get_field('location').max_length
        self.assertEqual(max_length, 40)

    def test_object_name_post_id(self):
        expected_object_name = f'Post#{self.post.id}'
        self.assertEquals(expected_object_name, str(self.post))

    def test_get_absolute_url(self):
        self.assertEquals(self.post.get_absolute_url(), '/post/1/')
