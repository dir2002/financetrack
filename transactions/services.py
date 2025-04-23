from .models import OpeningBalance, Transaction
from django.db.models import Sum
from decimal import Decimal

def calculate_cash_balance(user):
    try:
        cash_start = OpeningBalance.objects.get(user=user).cash_start_saldo
    except OpeningBalance.DoesNotExist:
        cash_start = Decimal('0.00')

    plus_ids = [25, 27, 28, 30]
    minus_ids = [24, 26, 29, 31]

    incomes = Transaction.objects.filter(user=user, category__name='Доходы').aggregate(total=Sum("amount"))["total"] or Decimal('0.00')
    expenses = Transaction.objects.filter(user=user, category__name='Расходы').aggregate(total=Sum("amount"))["total"] or Decimal('0.00')
    add_sum = Transaction.objects.filter(user=user, subcategory__id__in=plus_ids).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')
    sub_sum = Transaction.objects.filter(user=user, subcategory__id__in=minus_ids).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')

    total_cash_start = cash_start + incomes + add_sum - expenses - sub_sum

    return total_cash_start

def calculate_deposit_balance(user):
    try:
        deposit_start = OpeningBalance.objects.get(user=user).deposit_start_saldo
    except OpeningBalance.DoesNotExist:
        deposit_start = Decimal('0.00')

    plus_ids = [24]
    minus_ids = [25]
    add_sum = Transaction.objects.filter(user=user, subcategory__id__in=plus_ids).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')
    sub_sum = Transaction.objects.filter(user=user, subcategory__id__in=minus_ids).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')

    total_deposit_start = deposit_start + add_sum - sub_sum

    return total_deposit_start

def calculate_invest_balance(user):
    try:
        invest_start = OpeningBalance.objects.get(user=user).investment_start_saldo
    except OpeningBalance.DoesNotExist:
        invest_start = Decimal('0.00')

    plus_ids = [26]
    minus_ids = [27]
    add_sum = Transaction.objects.filter(user=user, subcategory__id__in=plus_ids).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')
    sub_sum = Transaction.objects.filter(user=user, subcategory__id__in=minus_ids).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')

    total_invest_start = invest_start + add_sum - sub_sum

    return total_invest_start

def calculate_short_debt_balance(user):
    try:
        short_debt_start = OpeningBalance.objects.get(user=user).short_debt_start_saldo
    except OpeningBalance.DoesNotExist:
        short_debt_start = Decimal('0.00')

    plus_ids = [28]
    minus_ids = [29]
    add_sum = Transaction.objects.filter(user=user, subcategory__id__in=plus_ids).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')
    sub_sum = Transaction.objects.filter(user=user, subcategory__id__in=minus_ids).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')

    total_short_debt_start = short_debt_start + add_sum - sub_sum

    return total_short_debt_start

def calculate_long_debt_balance(user):
    try:
        long_debt_start = OpeningBalance.objects.get(user=user).long_debt_start_saldo
    except OpeningBalance.DoesNotExist:
        long_debt_start = Decimal('0.00')

    plus_ids = [30]
    minus_ids = [31]
    add_sum = Transaction.objects.filter(user=user, subcategory__id__in=plus_ids).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')
    sub_sum = Transaction.objects.filter(user=user, subcategory__id__in=minus_ids).aggregate(total=Sum("amount"))["total"] or Decimal('0.00')

    total_long_debt_start = long_debt_start + add_sum - sub_sum

    return total_long_debt_start