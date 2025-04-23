from django.db import models
from datetime import date
from django.db.models import Sum

from users.models import User
from transactions.models import Category, SubCategory, Transaction

class BudgetLimit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    limit_amount = models.DecimalField('Сумма статьи', max_digits=10, decimal_places=2)
    start_date = models.DateField('Дата начала периода', blank=True, null=True,)
    end_date = models.DateField('Дата завершения периода', blank=True, null=True,)
    add_date = models.DateField('Дата создания', auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "category", "subcategory"],
                name="unique_user_category_subcategory_limit"
            )
        ]

    def calculate_actual_amount(self):
        transactions_sum = Transaction.objects.filter(user=self.user, subcategory=self.subcategory, date__gte=self.start_date, date__lte=self.end_date).aggregate(Sum('amount'))['amount__sum'] or 0
        return transactions_sum
    
    def calculate_limit_saldo_amount(self):
        return self.limit_amount - self.calculate_actual_amount()
    
    def calculate_days(self):
        days_left = (self.end_date - date.today()).days
        return max(days_left, 0) 
    
    def limit_status(self):
        return "Не действует" if self.end_date < date.today() else "Действует"




