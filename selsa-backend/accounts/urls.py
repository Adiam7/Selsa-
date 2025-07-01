from django.urls import path, include
from . import views
from .views import dashboard_view  # Import the dashboard view
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token  # Import the obtain_auth_token view

urlpatterns = [

    path('', views.home_view, name="home"),
    path('register/', views.register, name="register"),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path("password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('profile/', views.profile, name='profile'),
    path("api/auth/login/", obtain_auth_token)  # or your custom login view

]

