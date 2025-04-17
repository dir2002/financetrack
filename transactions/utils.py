from .models import OpeningBalance

# Эта функция готовит нужные данные и возвращает словарь в profile_view, 
# чтобы не перегружать данное представление лишними логикой и кодом

def get_opening_balance_context(user):
    balance, created = OpeningBalance.objects.get_or_create(user=user)

    return {
        'cash_start_saldo': balance.cash_start_saldo,
        'deposit_start_saldo': balance.deposit_start_saldo,
        'investment_start_saldo': balance.investment_start_saldo,
        'short_debt_start_saldo': balance.short_debt_start_saldo,
        'long_debt_start_saldo': balance.long_debt_start_saldo,
    }