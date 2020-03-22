from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from social.models import Post
from users.models import Profile, User


class ProfileDetailListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email='kornel@mail.com',
                                       username='kornel1')
        cls.password = 'temporary'
        cls.user.set_password(cls.password)
        cls.user.is_active = True
        cls.user.save()

        cls.profile = cls.user.profile
        cls.profile.bio = 'Northen man'
        cls.profile.city = 'Stockholm'
        cls.profile.website = 'facebook.com'

    def test_view_url_accessible_by_name(self):
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_pagination_is_off(self):
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'] == False)

    # TODO Turn pagination ON in social.views.PostListView
    # def test_pagination_is_on(self):
    #     self.client.login(email=self.user.email, password=self.password)
    #     response = self.client.get(
    #         reverse('profile', kwargs={'username': self.user.username}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(response.context['is_paginated'] == True)

    # def test_pagination_is_ten(self):
    #     self.client.login(email=self.user.email, password=self.password)
    #     response = self.client.get(
    #         reverse('profile', kwargs={'username': self.user.username}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     self.assertEquals(len(response.context['posts']), 10)
    #     self.assertTrue(len(response.context['posts']) == 10)

    # def test_lists_all_authors(self):
    #     self.client.login(email=self.user.email, password=self.password)
    #     # Get second page and confirm it has (exactly) remaining 3 items
    #     response = self.client.get(
    #         reverse('profile' + '?page=2',
    #                 kwargs={'username': self.user.username}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     self.assertTrue(len(response.context['posts']) == 3)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))
        self.assertRedirects(response, f'/login/?next=/{self.user.username}/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))

        self.assertEqual(str(response.context['user']), self.user.email)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'users/profile.html')

    def test_posts_on_profile_page_belong_only_to_the_user(self):
        self.client.login(email=self.user.email, password=self.password)

        user2 = User.objects.create(email='user2@mail.com', username='user2')
        user3 = User.objects.create(email='user3@mail.com', username='user3')

        post1 = Post.objects.create(
            author=self.profile,
            content='Post 1',
            date_posted=timezone.now(),
        )
        post2 = Post.objects.create(
            author=user2.profile,
            content='Post 2',
            date_posted=timezone.now(),
        )
        post3 = Post.objects.create(
            author=user3.profile,
            content='Post 3',
            date_posted=timezone.now(),
        )

        self.profile.add_follow(user2.profile)

        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))

        self.assertEqual(str(response.context['user']), self.user.email)
        self.assertEqual(response.status_code, 200)

        for post in response.context['posts']:
            self.assertTrue(response.context['user'] == post.author.user)

    def test_posts_ordered_by_newest(self):
        self.client.login(email=self.user.email, password=self.password)

        post1 = Post.objects.create(
            author=self.profile,
            content='Post 1',
            date_posted=timezone.now(),
        )
        post2 = Post.objects.create(
            author=self.profile,
            content='Post 2',
            date_posted=timezone.now(),
        )
        post3 = Post.objects.create(
            author=self.profile,
            content='Post 3',
            date_posted=timezone.now(),
        )

        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username}))

        self.assertEqual(str(response.context['user']), self.user.email)
        self.assertEqual(response.status_code, 200)

        last_date = 0

        posts = response.context['posts']
        posts = posts.reverse()

        for post in posts:
            if last_date == 0:
                last_date = post.date_posted
            else:
                self.assertTrue(last_date <= post.date_posted)
                last_date = post.date_posted

    def test_no_posts_at_profile(self):
        user = User.objects.create(email='user@mail.com', username='user')
        password = 'temporary'
        user.set_password(password)
        user.is_active = True
        user.save()
        self.client.login(email=user.email, password=password)

        response = self.client.get(
            reverse('profile', kwargs={'username': user.username}))

        self.assertEqual(str(response.context['user']), user.email)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['posts'], [])
