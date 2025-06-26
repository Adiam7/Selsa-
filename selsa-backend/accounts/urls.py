from django.urls import path, include
from . import views
from .views import dashboard_view  # Import the dashboard view
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

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

    #path('profile/edit/', views.edit_profile_view, name='edit_profile'),    
    #path('profile/password/', views.change_password_view, name='change_password'),
    #path('profile/delete/', views.delete_user_view, name='delete_user'),
    #path('profile/activate/', views.activate_user_view, name='activate_user'),
    #path('profile/deactivate/', views.deactivate_user_view, name='deactivate_user'),
    
    #path('invitations/', include('invitations.urls', namespace='invitations')),  # Invitations
    #path('accounts/', include('allauth.urls')),  # Allauth
    #path('accounts/', include('django.contrib.auth.urls')),  # Django auth
    #path('two_factor/', include('two_factor.urls', 'two_factor')),  # Two-factor authentication
    #path('social-auth/', include('social_django.urls', namespace='social')),  # Social auth
    #path('admin/', admin.site.urls),  # Admin

]

