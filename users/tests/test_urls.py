from django.test import TestCase
from django.urls import resolve, reverse
from django.urls.exceptions import NoReverseMatch

from social.views import PostCreateView, PostDetail, PostListView


class TestUrls(TestCase):
    def test_post_list_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, PostListView)

    def test_post_create_url_resolves(self):
        url = reverse('post-create')
        self.assertEquals(resolve(url).func.view_class, PostCreateView)

    def test_post_detail_url_resolves(self):
        url = reverse('post-detail', args=['10'])
        self.assertEquals(resolve(url).func.view_class, PostDetail)

    def test_post_detail_url_no_reverse_match(self):
        with self.assertRaises(NoReverseMatch):
            reverse('post-detail', args=['post15'])
