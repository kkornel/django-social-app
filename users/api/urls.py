from django.urls import path

from .views import ProfileDetailAPiView, ProfileListAPiView

urlpatterns = [
    path('profile/<str:username>/',
         ProfileDetailAPiView.as_view(),
         name='profile-detail'),
    path('profiles/', ProfileListAPiView.as_view(), name='profiles'),
]
