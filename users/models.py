from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    is_active = models.BooleanField(default=False)
    username = models.CharField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Картинка профиля")  
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="Номер телефона")
    cash_start_saldo = models.IntegerField(default=0, blank=True, verbose_name="Сумма денежных средств в наличии")
    deposit_start_saldo = models.IntegerField(default=0, blank=True, verbose_name="Сумма денег на депозитных счетах")
    investment_start_saldo = models.IntegerField(default=0, blank=True, verbose_name="Сумма денег в инвестиционных активах")
    short_debt_start_saldo = models.IntegerField(default=0, blank=True, verbose_name="Сумма долгов с возвратом в течение 12 мес")
    long_debt_start_saldo = models.IntegerField(default=0, blank=True, verbose_name="Сумма долгов с возвратом в течение более 12 мес")
    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, verbose_name="Фамилия")
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
   
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.is_active}"
    
    def save(self, *args, **kwargs):
        if not self.pk and self.is_superuser:  
            self.is_active = True
        for field in ['cash_start_saldo', 'deposit_start_saldo', 'investment_start_saldo',
                  'short_debt_start_saldo', 'long_debt_start_saldo']:
            if not getattr(self, field):  
                setattr(self, field, 0)
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