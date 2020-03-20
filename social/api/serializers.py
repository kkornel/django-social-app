import logging

from rest_framework import serializers

from social.models import Comment, Like, Post

logger = logging.getLogger(__name__)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_username')
    num_of_likes = serializers.SerializerMethodField('get_likes_count')
    likes = serializers.SerializerMethodField('get_likes')
    num_of_commetnts = serializers.SerializerMethodField('get_comments_count')
    comments = serializers.SerializerMethodField('get_comments')

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'content',
            'date_posted',
            'location',
            'image',
            'num_of_likes',
            'likes',
            'num_of_commetnts',
            'comments',
        ]

    def get_author_username(self, post):
        return post.author.user.username

    def get_likes_count(self, post):
        return post.likes.all().count()

    def get_likes(self, post):
        likes = []
        for like in Like.objects.filter(post=post):
            serializer = LikeSerializer(like)
            likes.append(serializer.data)
        return likes

    def get_comments_count(self, post):
        return post.comments.all().count()

    def get_comments(self, post):
        comments = []
        for comment in post.comments.values():
            comment = Comment.objects.get(pk=comment['id'])
            serializer = CommentSerializer(comment)
            comments.append(serializer.data)
        return comments


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_username')

    class Meta:
        model = Comment
        fields = ['author', 'text', 'date_commented']

    def get_author_username(self, comment):
        return comment.author.user.username


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_username')

    class Meta:
        model = Like
        fields = ['author', 'date_liked']

    def get_author_username(self, like):
        return like.author.user.username
