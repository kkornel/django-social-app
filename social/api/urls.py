from django.urls import path

from .views import PostDetailApiView, PostListAPiView

urlpatterns = [
    path('posts/', PostListAPiView.as_view(), name='posts'),
    path('post/<int:id>/', PostDetailApiView.as_view(), name='post-detail'),
]
