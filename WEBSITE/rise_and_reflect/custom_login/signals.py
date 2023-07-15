# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import UserProfile
# from django.conf import settings


# User = settings.AUTH_USER_MODEL

# @receiver(post_save, sender=UserProfile)
# def create_user_profile(sender, instance, **kwargs):
#     name = instance.name
#     phone = instance.phone
#     print(name)
#     print(instance.user.username)
#     # The bio field is not set because the User instance has not bio attribute by default.
#     # But you can still update this attribute with the profile detail form.
#     UserProfile.objects.create(user=instance.user, name=name, phone=phone)
