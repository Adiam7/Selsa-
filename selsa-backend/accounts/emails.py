from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    link = f"{settings.FRONTEND_URL}/verify-email/{user.verification_token}/"
    send_mail(
        'Verify your email',
        f'Click here to verify: {link}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )

def send_reset_password_email(user):
    link = f"{settings.FRONTEND_URL}/reset-password/{user.verification_token}/"
    send_mail(
        'Reset your password',
        f'Click here to reset: {link}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_welcome_email(user):
    send_mail(
        'Welcome to SELSA',
        'Thank you for joining SELSA! We are excited to have you on board.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_account_deletion_email(user):
    send_mail(
        'Account Deletion Confirmation',
        'Your account has been successfully deleted. We are sorry to see you go.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_email_change_notification(old_email, new_email):
    send_mail(
        'Email Change Notification',
        f'Your email has been changed from {old_email} to {new_email}. If this was not you, please contact support.',
        settings.DEFAULT_FROM_EMAIL,
        [new_email],
    )
def send_password_change_notification(user):
    send_mail(
        'Password Change Notification',
        'Your password has been changed successfully. If this was not you, please contact support.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_account_recovery_email(user):
    link = f"{settings.FRONTEND_URL}/recover-account/{user.verification_token}/"
    send_mail(
        'Account Recovery',
        f'Click here to recover your account: {link}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )   
def send_two_factor_authentication_code(user, code):
    send_mail(
        'Two-Factor Authentication Code',
        f'Your two-factor authentication code is: {code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_subscription_confirmation_email(user, subscription_details):
    send_mail(
        'Subscription Confirmation',
        f'Thank you for subscribing! Here are your subscription details: {subscription_details}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_subscription_cancellation_email(user):
    send_mail(
        'Subscription Cancellation',
        'Your subscription has been successfully cancelled. We hope to see you back soon!',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_newsletter_subscription_email(user):
    send_mail(
        'Newsletter Subscription',
        'Thank you for subscribing to our newsletter! You will receive updates and news from us.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_newsletter_unsubscription_email(user):
    send_mail(
        'Newsletter Unsubscription',
        'You have successfully unsubscribed from our newsletter. We are sorry to see you go!',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_event_invitation_email(user, event_details):
    send_mail(
        'Event Invitation',
        f'You are invited to the following event: {event_details}. We hope to see you there!',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_event_reminder_email(user, event_details):
    send_mail(
        'Event Reminder',
        f'Reminder: You have an upcoming event: {event_details}. We look forward to your participation!',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_feedback_request_email(user):
    send_mail(
        'Feedback Request',
        'We value your feedback! Please take a moment to share your thoughts with us.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_survey_invitation_email(user, survey_link):
    send_mail(
        'Survey Invitation',
        f'We invite you to participate in our survey: {survey_link}. Your feedback is important to us!',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_system_notification_email(user, notification_message): 
    send_mail(
        'System Notification',
        f'Important system notification: {notification_message}. Please take note of this information.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_security_alert_email(user, alert_message):
    send_mail(
        'Security Alert',
        f'Important security alert: {alert_message}. Please take immediate action if necessary.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_account_activity_notification_email(user, activity_details):
    send_mail(
        'Account Activity Notification',
        f'You have new activity on your account: {activity_details}. Please review your account for any unauthorized actions.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
def send_custom_email(user, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )   
# This function can be used to send custom emails with specific subjects and messages.
# It can be useful for sending personalized notifications or updates to users.  
# Example usage:
# send_custom_email(user, 'Custom Subject', 'This is a custom message for the user.')
# This will send an email to the user with the specified subject and message.
# Make sure to replace `user` with the actual user object when calling this function.
