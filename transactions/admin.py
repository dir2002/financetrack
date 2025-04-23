from django.contrib import admin
from .models import Category, OpeningBalance, SubCategory, Transaction


@admin.register(OpeningBalance)
class OpeningBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'cash_start_saldo', 'deposit_start_saldo', 'investment_start_saldo', 'short_debt_start_saldo', 'long_debt_start_saldo', 'date_saldo_update')
    search_fields = ('user', 'cash_start_saldo', 'deposit_start_saldo', 'investment_start_saldo', 'short_debt_start_saldo', 'long_debt_start_saldo', 'date_saldo_update')
    list_filter = ('user', 'date_saldo_update')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'subcategory', 'amount', 'date')
    search_fields = ('user', 'category', 'subcategory', 'amount', 'date')
    list_filter = ('user', 'category','date')

admin.site.register(Category)
admin.site.register(SubCategory)