"""djangoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from users import admin as users_admin
from users import forms as users_forms
from users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', users_views.home, name='home'),
    path('register/', users_views.register, name='register'),
    path('activate/<uidb64>/<token>/',
         users_views.activate_account,
         name='activate'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='users/login.html',
             authentication_form=users_admin.CustomAuthenticationForm,
             redirect_authenticated_user=True),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # My custom way in order to style add reCAPTCHA and validate it.
    path('password-reset/', users_views.reset_password, name='password_reset'),
    # Default way, Corey showed this:
    # path('password-reset/',
    #  auth_views.PasswordResetView.as_view(
    #  template_name='users/password_reset.html'),
    #  name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    # My custom way in order to style input.
    path(
        'password-reset-confirm/<uidb64>/<token>/',  # after pressing button on reset password, Django tries to go to this route but it does not exist, so we are creating it here. It also takes 2 parameters. uidb64 and token which ensures that person who is calling it is actually that person.
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            form_class=users_forms.CustomSetPasswordForm),
        name='password_reset_confirm'),
    # Default way, Corey showed this:
    # path('password-reset-confirm/<uidb64>/<token>/',  # after pressing button on reset password, Django tries to go to this route but it does not exist, so we are creating it here. It also takes 2 parameters. uidb64 and token which ensures that person who is calling it is actually that person.
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='users/password_reset_confirm.html'),
    #      name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]