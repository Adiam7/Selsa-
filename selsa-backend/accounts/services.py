from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .emails import send_verification_email, send_reset_password_email

User = get_user_model()

def create_user(data):
    user = User.objects.create_user(**data)
    send_verification_email(user)
    return user

def verify_user_email(token):
    try:
        user = User.objects.get(verification_token=token)
        user.is_email_verified = True
        user.verification_token = None
        user.save()
        return user
    except User.DoesNotExist:
        raise ValueError("Invalid token")

def initiate_password_reset(email):
    try:
        user = User.objects.get(email=email)
        send_reset_password_email(user)
    except ObjectDoesNotExist:
        pass  # Do not leak user info

def confirm_password_reset(token, new_password):
    try:
        user = User.objects.get(verification_token=token)
        user.set_password(new_password)
        user.verification_token = None
        user.save()
    except User.DoesNotExist:
        raise ValueError("Invalid or expired token")

def change_user_password(user, old_password, new_password):
    if not user.is_authenticated:
        raise ValueError("User must be authenticated to change password")   
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return True
    else:
        raise ValueError("Old password is incorrect")

def get_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

def get_user_by_id(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None 
    
def reset_password_request(email):
    user = get_user_by_email(email)
    if user:
        user.verification_token = user.generate_verification_token()
        user.save()
        send_reset_password_email(user)
        return True
    return False

def reset_password_confirm(token, new_password):
    try:
        user = User.objects.get(verification_token=token)
        user.set_password(new_password)
        user.verification_token = None
        user.save()
        return True
    except User.DoesNotExist:
        return False    
    
def change_password(user, old_password, new_password):
    if not user.check_password(old_password):
        raise ValueError("Old password is incorrect")
    user.set_password(new_password)
    user.save()
    return True