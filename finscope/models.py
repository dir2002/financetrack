from datetime import date
from django.db import models

from users.models import User


class Task(models.Model):
    name = models.CharField("Название задания", max_length=255)
    description = models.TextField("Описание")
    deadline = models.DateField('Срок задания')
    finscore = models.IntegerField('FinScores', default=0)
    is_active = models.BooleanField(default=True)
    add_date = models.DateField('Дата создания', default=date.today)
    task_participants = models.ManyToManyField(User, blank=True, verbose_name='Участники курса', related_name='tasks')
    

    def __str__(self):
            return f"({self.name} ({self.finscore} баллов)"
    
