from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from .models import User

# Используем функцию сигнала, чтобы при удалении 
# пользователя, удалялись также его аватарки
@receiver(post_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    if instance.avatar:
        avatar_path = instance.avatar.path
        if os.path.isfile(avatar_path):
            os.remove(avatar_path)