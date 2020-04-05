from django.urls import path

from .views import (ProfileDetailAPiView, ProfileListAPiView,
                    UserDetailAPiView, UserListApiView)

urlpatterns = [
    path('users/', UserListApiView.as_view(), name='api-users'),
    path('user/<str:username>/',
         UserDetailAPiView.as_view(),
         name='api-user-detail'),
    path('profiles/', ProfileListAPiView.as_view(), name='api-profiles'),
    path('profile/<str:username>/',
         ProfileDetailAPiView.as_view(),
         name='api-profile-detail'),
]
