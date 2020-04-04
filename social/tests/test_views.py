import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from social.models import Post
from users.models import Profile, User


class PostListViewTest(TestCase):
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

        # Create 13 posts for pagination tests
        number_of_posts = 13

        for post_id in range(number_of_posts):
            Post.objects.create(
                author=cls.profile,
                content='Learning tests in Django Framework',
                date_posted=timezone.now(),
                location='Tomaszów Mazowiecki',
            )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/home.html')

    def test_pagination_is_off(self):
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'] == False)

    # TODO Turn pagination ON in social.views.PostListView
    # def test_pagination_is_on(self):
    #     self.client.login(email=self.user.email, password=self.password)
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(response.context['is_paginated'] == True)

    # def test_pagination_is_ten(self):
    #     self.client.login(email=self.user.email, password=self.password)
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     self.assertEquals(len(response.context['posts']), 10)
    #     self.assertTrue(len(response.context['posts']) == 10)

    # def test_lists_all_authors(self):
    #     self.client.login(email=self.user.email, password=self.password)
    #     # Get second page and confirm it has (exactly) remaining 3 items
    #     response = self.client.get(reverse('home') + '?page=2')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     self.assertTrue(len(response.context['posts']) == 3)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/login/?next=/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(email=self.user.email, password=self.password)
        response = self.client.get(reverse('home'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), self.user.email)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'social/home.html')

    def test_posts_on_home_page_belong_only_to_the_user_and_followers(self):
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

        response = self.client.get(reverse('home'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), self.user.email)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        for post in response.context['posts']:
            self.assertTrue(
                response.context['user'] == post.author.user or
                post.author in response.context['user'].profile.get_followed())

    def test_posts_ordered_by_newest(self):
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

        response = self.client.get(reverse('home'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), self.user.email)
        # Check that we got a response "success"
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

    def test_no_posts_at_home(self):
        user = User.objects.create(email='user@mail.com', username='user')
        password = 'temporary'
        user.set_password(password)
        user.is_active = True
        user.save()
        self.client.login(email=user.email, password=password)

        response = self.client.get(reverse('home'))

        self.assertEqual(str(response.context['user']), user.email)
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(response.context['posts'], [])


class PostUpdateViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='user1@mail.com',
                                         username='user1')
        self.user2 = User.objects.create(email='user2@mail.com',
                                         username='user2')
        self.password1 = 'temporary'
        self.password2 = 'temporary'
        self.user1.set_password(self.password1)
        self.user2.set_password(self.password2)
        self.user1.is_active = True
        self.user2.is_active = True
        self.user1.save()
        self.user2.save()

        self.profile1 = self.user1.profile
        self.profile2 = self.user2.profile

        self.post1 = Post.objects.create(
            author=self.profile1,
            content='Post1',
            date_posted=timezone.now(),
            location='Tomaszów Mazowiecki',
        )
        self.post2 = Post.objects.create(
            author=self.profile2,
            content='Post2',
            date_posted=timezone.now(),
            location='Tomaszów Mazowiecki',
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('post-update', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_redirect_if_logged_in_but_not_correct_persmission(self):
        self.client.login(email=self.user1.email, password=self.password1)
        response = self.client.get(
            reverse('post-update', kwargs={'pk': self.post2.id}))
        self.assertEqual(response.status_code, 403)

    def test_logged_in_with_permission_granted(self):
        self.client.login(email=self.user1.email, password=self.password1)
        response = self.client.get(
            reverse('post-update', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_post_if_logged_in(self):
        # unlikely UID to match our bookinstance!
        test_uid = 6786856
        self.client.login(email=self.user1.email, password=self.password1)
        response = self.client.get(
            reverse('post-update', kwargs={'pk': test_uid}))
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        self.client.login(email=self.user1.email, password=self.password1)
        response = self.client.get(
            reverse('post-update', kwargs={'pk': self.post1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'social/post_update.html')

    def test_redirects_to_post_detail_on_success(self):
        self.client.login(email=self.user1.email, password=self.password1)

        response = self.client.post(
            reverse('post-update', kwargs={'pk': self.post1.id}))
        self.assertRedirects(
            response, reverse('post-detail', kwargs={'pk': self.post1.id}))


class PostCreateViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='user1@mail.com',
                                         username='user1')
        self.password1 = 'temporary'
        self.user1.set_password(self.password1)
        self.user1.is_active = True
        self.user1.save()

    def test_post_create_POST(self):
        self.client.login(email=self.user1.email, password=self.password1)
        url = reverse('post-create')
        response = self.client.post(
            url, {
                'author': self.user1.profile,
                'content': 'TEST',
                'date_posted': timezone.now(),
                'location': 'Tomaszów Mazowiecki',
            })
        post = Post.objects.get(pk=2)
        self.assertEqual(post.author, self.user1.profile)
        self.assertEquals(post.content, 'TEST')
