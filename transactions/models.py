from django.db import models
from django.utils import timezone
import datetime

from users.models import User



class OpeningBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cash_start_saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, verbose_name="Сумма денежных средств в наличии")
    deposit_start_saldo = models.DecimalField(max_digits=12, decimal_places=2,default=0, blank=True, verbose_name="Сумма денег на депозитных счетах")
    investment_start_saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, verbose_name="Сумма денег в инвестиционных активах")
    short_debt_start_saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, verbose_name="Сумма долгов с возвратом в течение 12 мес")
    long_debt_start_saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, verbose_name="Сумма долгов с возвратом в течение более 12 мес")
    date_saldo_update = models.DateTimeField(default=timezone.now)
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Категория")

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Подкатегория", default="Без названия")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Transaction(models.Model):
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма транзакции")
    date = models.DateField(blank=True, null=True, default=datetime.date.today, verbose_name="Дата транзакции")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, verbose_name="Описание транзакции")

    def __str__(self):
        return f"{self.amount} - {self.category} - {self.subcategory}"