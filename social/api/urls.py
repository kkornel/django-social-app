from django.urls import path

from .views import (CommentDetailApiView, CommentListApiView,
                    LikeDetailApiView, LikeListApiView, PostDetailApiView,
                    PostListAPiView)

urlpatterns = [
    path('posts/', PostListAPiView.as_view(), name='api-posts'),
    path('post/<int:id>/', PostDetailApiView.as_view(),
         name='api-post-detail'),
    path('comments/', CommentListApiView.as_view(), name='api-comments'),
    path('comment/<int:id>/',
         CommentDetailApiView.as_view(),
         name='api-comment-detail'),
    path('likes/', LikeListApiView.as_view(), name='api-like'),
    path('like/<int:id>/', LikeDetailApiView.as_view(),
         name='api-like-detail'),
]
