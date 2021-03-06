import logging

from rest_framework import serializers

from social.api.serializers import (CommentSerializer, LikeSerializer,
                                    PostSerializer)
from social.models import Like
from users.models import Profile, User

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined']


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')

    followers = serializers.SerializerMethodField('get_followers')
    followers_count = serializers.SerializerMethodField('get_followers_count')

    following = serializers.SerializerMethodField('get_followed')
    following_count = serializers.SerializerMethodField('get_followed_count')

    posts = serializers.SerializerMethodField('get_posts')
    posts_count = serializers.SerializerMethodField('get_posts_count')

    comments = serializers.SerializerMethodField('get_comments')
    comments_count = serializers.SerializerMethodField('get_comments_count')

    likes = serializers.SerializerMethodField('get_likes')
    likes_count = serializers.SerializerMethodField('get_likes_count')

    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'bio',
            'city',
            'website',
            'image',
            'followers',
            'followers_count',
            'following',
            'following_count',
            'posts',
            'posts_count',
            'comments',
            'comments_count',
            'likes',
            'likes_count',
        ]

    def get_username(self, profile):
        return profile.user.username

    def get_followers(self, profile):
        followers = []
        for follower in profile.followers.all():
            followers.append(follower.user.username)
        return followers

    def get_followers_count(self, profile):
        return profile.followers.all().count()

    def get_followed(self, profile):
        following = []
        for follow in profile.get_followed():
            following.append(follow.user.username)
        return following

    def get_followed_count(self, profile):
        return profile.get_followed().count()

    def get_posts(self, profile):
        posts = []
        # for post in profile.posts.all():
        #     serializer = PostSerializer(post)
        #     posts.append(serializer.data)
        for post in profile.posts.all():
            posts.append(post.pk)
        return posts

    def get_posts_count(self, profile):
        return profile.posts.all().count()

    def get_comments(self, profile):
        comments = []
        # for comment in profile.comments.all():
        #     serializer = CommentSerializer(comment)
        #     comments.append(serializer.data)
        for comment in profile.comments.all():
            comments.append(comment.pk)
        return comments

    def get_comments_count(self, profile):
        return profile.comments.all().count()

    def get_likes(self, profile):
        likes = []
        # for like in Like.objects.filter(author=profile):
        #     serializer = LikeSerializer(like)
        #     likes.append(serializer.data)
        for like in Like.objects.filter(author=profile):
            likes.append(like.pk)
        return likes

    def get_likes_count(self, profile):
        return profile.likes.all().count()
