from django.urls import path

from .views import ProfileDetailAPiView

urlpatterns = [
    path('<str:username>/',
         ProfileDetailAPiView.as_view(),
         name='profile-detail'),
]
