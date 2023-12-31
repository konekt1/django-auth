import random
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from djangoauth import settings
from .models import InternProfile, RecruiterProfile, User
from decouple import config

def send_otp_email(user):
    otp_code = random.randint(100000, 999999)  # Generate a random 6-digit OTP code

    user.otp = otp_code
    user.save()  # The otp code will be saved the user model otp field


    # Send the OTP code via email
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp_code}'
    from_email = config('EMAIL_USER')
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == "intern":
            InternProfile.objects.create(user=instance)
        elif instance.role == "recruiter":
            RecruiterProfile.objects.create(user=instance)



@receiver(post_save, sender=User)
def send_otp_on_registration(sender, instance, created, **kwargs):
    if created:
        send_otp_email(instance)  # Send OTP email when a new user is created

