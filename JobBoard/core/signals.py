from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, EmployerProfile, SeekerProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_type = getattr(instance, 'user_type', None)
        profile = Profile.objects.create(user=instance, user_type=user_type)

        if user_type == 'employer':
            EmployerProfile.objects.create(user=instance)
        else:
            SeekerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        pass
