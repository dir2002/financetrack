from django.db import models
from users.models import User
from categories.models import Category, SubCategory


class Budget(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   