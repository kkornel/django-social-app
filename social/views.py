import json
import logging

from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalDeleteView, BSModalReadView,
                                           BSModalUpdateView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, reverse
from django.views import View, generic
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from social import forms as social_forms
from users.models import Profile, User

from .models import Comment, Post

logger = logging.getLogger(__name__)


class PostListView(LoginRequiredMixin, ListView):
    # model = Post
    # If not specified, Django looks for template in following path: '<app>/<model>_<viewtype>.html'
    template_name = 'social/home.html'
    # If not specified, Django uses name 'object' for data passed to template file.
    context_object_name = 'posts'
    ordering = ['-date_posted']

    # paginate_by = 10

    def get_queryset(self):
        posts_to_display = self.request.user.profile.posts.all()
        # logger.debug(posts_to_display.count())
        following = self.request.user.profile.follows.all()
        # logger.debug(following)
        for follow in following:
            # logger.debug(follow.posts.all().count())
            posts_to_display = posts_to_display | follow.posts.all()
        # logger.debug(posts_to_display.count())
        return posts_to_display.order_by('-date_posted')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # Specifying both 'fields' and 'form_class' is not permitted.
    form_class = social_forms.PostCreateForm
    # Either form_class or fields.
    # fields = ['content', 'location', 'image']
    # We do not have to specify template_name, because Django uses post_form.html,
    # for both: CreateView and UpdateView. No need to create seperate.
    template_name = 'social/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class PostCreateViewModal(PostCreateView, BSModalCreateView):
    template_name = 'social/post_create_modal.html'
    form_class = social_forms.PostCreateFormModal
    success_message = ''

    def get_success_url(self):
        return reverse('post-detail', args=(self.object.id, ))


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    # Specifying both 'fields' and 'form_class' is not permitted.
    form_class = social_forms.PostUpdateForm
    # Either form_class or fields
    # fields = ['content', 'location', 'image']
    template_name = 'social/post_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        delete_current_image = form.cleaned_data['delete_current_image']
        image = form.instance.image
        if delete_current_image and not image:
            logger.debug('Tried to delete image from post with no image.')
        if delete_current_image and image:
            logger.debug(f'Removing image: {image}...')
            image.delete(save=False)
            logger.debug(f'Image removed.')
        return super().form_valid(form)

    def test_func(self):
        """
        This function is run by UserPassesTestMixin to check something that we want to check.
        In this case we want to check if the currently logged in user is also the author of the post.
        If he is not, then he has no permissions to do that.
        """
        post = self.get_object()
        return self.request.user.profile == post.author


class PostUpdateViewModal(PostUpdateView, BSModalUpdateView):
    form_class = social_forms.PostUpdateFormModal
    template_name = 'social/post_update_modal.html'
    success_message = ''

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'
    success_url = '/'  # Where to go after deleting.

    def test_func(self):
        post = self.get_object()
        return self.request.user.profile == post.author


class PostDeleteViewModal(PostDeleteView, BSModalDeleteView):
    template_name = 'social/post_confirm_delete_modal.html'
    success_message = ''


class PostDetail(View):
    """https://docs.djangoproject.com/en/2.2/topics/class-based-views/mixins/#using-formmixin-with-detailview"""
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentCreateView.as_view()
        return view(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = social_forms.CommentCreateForm()
        return context


class CommentCreateView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Post
    form_class = social_forms.CommentCreateForm
    template_name = 'social/post_detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class CommentCreateViewModal(LoginRequiredMixin, BSModalCreateView):
    model = Post
    form_class = social_forms.CommentCreateFormModal
    template_name = 'social/comment_create_modal.html'

    def form_valid(self, form):
        # Here, unlike the solution in CommentCreateView, we have to query
        # for the post object, because it is not attached to the request.
        # So we use kwargs to get pk of that post object.
        form.instance.author = self.request.user.profile
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class CommentDeleteViewModal(BSModalDeleteView):
    model = Comment
    template_name = 'social/comment_confirm_delete_modal.html'
    success_message = ''

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


@login_required
def like_post(request):
    if request.method == 'POST':
        postId = request.POST.get('postId')
        userId = request.POST.get('userId')

        post = Post.objects.get(pk=int(postId))
        profile = Profile.objects.get(pk=int(userId))

        if profile in post.likes.all():
            post.likes.remove(profile)
        else:
            post.likes.add(profile)

    response = post.likes.all().count()
    return HttpResponse(response)


@login_required
def follow_user(request):
    if request.method == 'POST':
        followerID = request.POST.get('followerID')
        followingID = request.POST.get('followingID')

        # logger.debug(followerID)
        # logger.debug(followingID)

        follower = Profile.objects.get(pk=int(followerID))
        following = Profile.objects.get(pk=int(followingID))

        # logger.debug(follower)
        # logger.debug(following)

        if follower.is_following(following):
            # logger.debug('Already following. Removing follow.')
            follower.remove_follow(following)
            # logger.debug(follower.get_following())
            # logger.debug(following.get_following())
            # logger.debug(follower.get_followers())
            # logger.debug(following.get_followers())

        else:
            # logger.debug('Adding follow.')
            follower.add_follow(following)
            # logger.debug(follower.get_following())
            # logger.debug(following.get_following())
            # logger.debug(follower.get_followers())
            # logger.debug(following.get_followers())

    followers = following.get_followers().count()
    following = following.get_following().count()
    response = {"followers": followers, "following": following}
    # logger.debug(response)
    return HttpResponse(json.dumps(response))


class FollowersView(ListView):
    template_name = 'social/followers.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        return user.profile.followers.all()


class FollowingView(FollowersView):
    template_name = 'social/following.html'

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        return user.profile.follows.all()
