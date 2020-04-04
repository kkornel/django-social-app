from django.test import TestCase

from users.models import Profile, User


class ProfileTestModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        """setUpTestData: Run once to set up non-modified data for all class methods."""
        cls.user = User.objects.create(email='kornel@mail.com',
                                       username='kornel1')
        cls.profile = cls.user.profile
        cls.profile.bio = 'Northen man'
        cls.profile.city = 'Stockholm'
        cls.profile.website = 'facebook.com'

    def setUp(self):
        """setUp: Run once for every test method to setup clean data."""
        self.user1 = User.objects.create(email='user1@mail.com',
                                         username='user1')
        self.user2 = User.objects.create(email='user2@mail.com',
                                         username='user2')

        self.profile1 = self.user1.profile
        self.profile2 = self.user2.profile

    def test_bio_label(self):
        field_label = self.profile._meta.get_field('bio').verbose_name
        self.assertEquals(field_label, 'bio')
        self.assertNotEquals(field_label, 'city')

    def test_city_max_length(self):
        max_length = self.profile._meta.get_field('city').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_profile_id_username(self):
        expected_object_name = f'Profile#{self.profile.id}.{self.profile.user.username}'
        self.assertEquals(expected_object_name, str(self.profile))

    def test_user1_following_user2(self):
        self.profile1.add_follow(self.profile2)
        self.assertIn(self.profile2, self.profile1.get_followed())
        self.assertIn(self.profile1, self.profile2.get_followers())
        self.assertNotIn(self.profile2, self.profile1.get_followers())
        self.assertNotIn(self.profile1, self.profile2.get_followed())
        self.assertTrue(self.profile1.is_following(self.profile2))
        self.assertFalse(self.profile2.is_following(self.profile1))
        self.assertTrue(self.profile2.is_followed_by(self.profile1))
        self.assertFalse(self.profile1.is_followed_by(self.profile2))
