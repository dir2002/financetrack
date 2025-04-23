from django.contrib import admin
from .models import BudgetLimit

@admin.register(BudgetLimit)
class BudgetLimitAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'subcategory', 'limit_amount', 'start_date', 'end_date', 'is_active')
    search_fields = ('user', 'category', 'subcategory', 'limit_amount', 'start_date', 'end_date', 'is_active')
    list_filter = ('user', 'category', 'subcategory', 'is_active')


