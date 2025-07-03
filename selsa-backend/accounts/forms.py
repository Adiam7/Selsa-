# auth/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # Optional phone number field for SMS-based two-factor authentication
    phone_number = forms.CharField(
        max_length=20, 
        required=False, 
        help_text="Optional. Enter your phone number for SMS-based 2FA."
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "password1", "password2")

class RegisterForm(CustomUserCreationForm):
    pass