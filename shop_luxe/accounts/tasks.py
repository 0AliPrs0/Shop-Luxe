from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

@shared_task
def send_verification_email(user_id, domain):
    try:
        user = User.objects.get(id=user_id)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        verification_path = reverse('email-verify', kwargs={'uidb64': uid, 'token': token})
        verification_url = f"http://{domain}{verification_path}"
        
        subject = 'Activate Your Account'
        message = f'Hi {user.username},\n\nPlease click the link below to activate your account:\n{verification_url}'
        
        send_mail(
            subject=subject,
            message=message,
            from_email='no-reply@yourshop.com',
            recipient_list=[user.email]
        )
        return f"Verification email sent for user {user.email}."
    except User.DoesNotExist:
        return f"User with ID {user_id} not found."

@shared_task
def send_password_reset_email(user_id, domain):
    try:
        user = User.objects.get(id=user_id)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # NOTE: Ensure you have a URL named 'password-reset-confirm-api' or similar
        reset_path = f"/api/accounts/password-reset/confirm/{uid}/{token}/" 
        reset_url = f"http://your-frontend-domain.com{reset_path}" # Frontend URL
        
        subject = 'Reset Your Password'
        message = f'Hi {user.username},\n\nPlease click the link to reset your password:\n{reset_url}'
        
        send_mail(
            subject=subject,
            message=message,
            from_email='no-reply@yourshop.com',
            recipient_list=[user.email]
        )
        return f"Password reset email sent for user {user.email}."
    except User.DoesNotExist:
        return f"User with ID {user_id} not found."