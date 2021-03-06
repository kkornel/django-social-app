from django.urls import path

from social import views as social_views

urlpatterns = [
    path('', social_views.PostListView.as_view(), name='home'),
    path('new/', social_views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/',
         social_views.PostDetail.as_view(),
         name='post-detail'),
    path('post/<int:pk>/update/',
         social_views.PostUpdateView.as_view(),
         name='post-update'),
    path('post/<int:pk>/delete/',
         social_views.PostDeleteView.as_view(),
         name='post-delete'),
    path('search/', social_views.search, name='search'),
    path('tags/<str:tag>/', social_views.search_tags, name='search-tags'),
    # AJAX
    path('like/', social_views.like_post, name='like-post'),
    path('follow/', social_views.follow_user, name='follow-user'),

    # Modals
    # Posts
    path('new-modal/',
         social_views.PostCreateViewModal.as_view(),
         name='post-create-modal'),
    path('post/<int:pk>/update-modal/',
         social_views.PostUpdateViewModal.as_view(),
         name='post-update-modal'),
    path('post/<int:pk>/delete-modal/',
         social_views.PostDeleteViewModal.as_view(),
         name='post-delete-modal'),
    # Comments
    path('post/<int:pk>/comment-new-modal/',
         social_views.CommentCreateViewModal.as_view(),
         name='comment-create-modal'),
    path('post/<int:pk>/comment-delete-modal/',
         social_views.CommentDeleteViewModal.as_view(),
         name='comment-delete-modal'),
    # Followers
    path('<str:username>/followers/',
         social_views.FollowersView.as_view(),
         name='followers'),
    path('<str:username>/following/',
         social_views.FollowingView.as_view(),
         name='following'),
]
