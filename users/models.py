from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import re
from django.core.exceptions import ValidationError

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    is_active = models.BooleanField(default=False)
    username = models.CharField(blank=True, null=True, verbose_name="Уникальный псевдоним")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Картинка профиля")  
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="Номер телефона")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    

    # меняем приоритет поля по умолчанию
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
   
    # добавляем функцию валидации полей на латиницу
    def clean(self):
        super().clean()
        pattern = r'^[a-zA-Z0-9_]+$'

        fields_to_check = {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

        for field_name, value in fields_to_check.items():
            if not re.match(pattern, value):
                raise ValidationError({field_name: f"{field_name} может содержать только латиницу, цифры и _"})

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email} - {self.is_active}"
    
    # добавляем условие для удобства, чтобы при создании нового пользователя суперпользователь должен быть активирован
    def save(self, *args, **kwargs):
        if not self.pk and self.is_superuser:  
            self.is_active = True
        super().save(*args, **kwargs)
  
def generate_token():
    return get_random_string(28)

class EmailActivation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True, default=generate_token)  
    is_active = models.BooleanField(default=False)
        
    def send_email(self):
        subject = 'Подтверждение email'
        message = f'Подтвердите свой email, перейдя по ссылке http://localhost:8000/users/activate/{self.token}/'
        from_email = 'admin@localhost'
        recipient_list = [self.user.email]

        print(f"Токен для подтверждения почты: {self.token}")

        send_mail(subject, message, from_email, recipient_list)


    def activate_user(token: str):
        activation = get_object_or_404(EmailActivation, token=token)
        user = activation.user
        user.is_active = True
        user.save()
        activation.delete()