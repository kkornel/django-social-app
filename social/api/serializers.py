import logging

from rest_framework import serializers

from social.models import Comment, Like, Post

logger = logging.getLogger(__name__)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_username')

    likes = serializers.SerializerMethodField('get_likes')
    likes_count = serializers.SerializerMethodField('get_likes_count')

    comments = serializers.SerializerMethodField('get_comments')
    comments_count = serializers.SerializerMethodField('get_comments_count')

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'content',
            'date_posted',
            'location',
            'image',
            'likes_count',
            'likes',
            'comments_count',
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
    post_id = serializers.SerializerMethodField('get_post_id')

    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'author', 'text', 'date_commented']

    def get_author_username(self, comment):
        return comment.author.user.username

    def get_post_id(self, comment):
        return comment.post.id


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_username')
    post_id = serializers.SerializerMethodField('get_post_id')

    class Meta:
        model = Like
        fields = ['id', 'post_id', 'author', 'date_liked']

    def get_author_username(self, like):
        return like.author.user.username

    def get_post_id(self, like):
        return like.post.id
