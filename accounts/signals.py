from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Profile, CustomUser

@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    '''This function is to let the user update his profile (email and username)'''
    print('reaches here')
    if created:
        Profile.objects.create(user=instance)

