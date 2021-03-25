from . models import Profile, CustomUser
from quiz.models import UserProgress
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    '''This function is to let the user update his profile (email and username)'''
    if created:
        Profile.objects.create(user=instance)

    UserProgress.objects.get_or_create(
        user=instance)


@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance, created, **kwargs):
    '''This function is create a token once a user is created'''
    if created:
        Token.objects.create(user=instance)