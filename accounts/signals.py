from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, SellerProfile, UserProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_seller:
            SellerProfile.objects.create(user=instance)
        else:
            UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_seller:
        instance.sellerprofile.save()
    else:
        instance.userprofile.save()
