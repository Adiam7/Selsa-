from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view()),
    path('auth/verify-email/<uuid:token>/', views.VerifyEmailView.as_view()),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/change-password/', views.ChangePasswordView.as_view()),
    path('auth/reset-password/', views.ResetPasswordRequestView.as_view()),
    path('auth/reset-password/confirm/', views.ResetPasswordConfirmView.as_view()),
    path('auth/forget-password/', views.forgetPasswordView.as_view()),
]
