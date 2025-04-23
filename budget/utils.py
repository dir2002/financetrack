from decimal import Decimal
from django.db.models import Sum, F, Q, Value, DecimalField
from django.db.models.functions import Coalesce
from .models import SubCategory


def calculate_total_incomes(user):
    incomes_summary = SubCategory.objects.filter(category__pk=1).annotate(
        total_planned=Coalesce(
            Sum("budgetlimit__limit_amount", filter=Q(budgetlimit__user=user), distinct=True),
            Value(Decimal('0.00')),
            output_field=DecimalField()
        ),
        total_actual=Coalesce(
            Sum("transaction__amount", filter=Q(transaction__user=user)),
            Value(Decimal('0.00')),
            output_field=DecimalField()
        ),
    ).annotate(
        difference=F("total_planned") - F("total_actual")
    )

    total_incomes = incomes_summary.aggregate(
        total_planned_sum=Sum('total_planned'),
        total_actual_sum=Sum('total_actual'),
        total_diff_sum=Sum('difference')
    )

    return total_incomes


def calculate_total_expenses(user):
    expenses_summary = SubCategory.objects.filter(category__pk=2).annotate(
        total_planned=Coalesce(
            Sum("budgetlimit__limit_amount", filter=Q(budgetlimit__user=user), distinct=True),
            Value(Decimal('0.00')),
            output_field=DecimalField()
        ),
        total_actual=Coalesce(
            Sum("transaction__amount", filter=Q(transaction__user=user)),
            Value(Decimal('0.00')),
            output_field=DecimalField()
        ),
    ).annotate(
        difference=F("total_planned") - F("total_actual")
    )

    total_expenses = expenses_summary.aggregate(
        total_planned_sum=Sum('total_planned'),
        total_actual_sum=Sum('total_actual'),
        total_diff_sum=Sum('difference')
    )

    return total_expenses


def calculate_total_result(user):
    total_incomes = calculate_total_incomes(user)
    total_expenses = calculate_total_expenses(user)

    total_result_planned = (total_incomes["total_planned_sum"] ) - (total_expenses["total_planned_sum"] )
    total_result_actual = (total_incomes["total_actual_sum"] ) - (total_expenses["total_actual_sum"] )
    total_result_diff = (total_incomes["total_diff_sum"] ) - (total_expenses["total_diff_sum"] )

    

    return total_result_planned, total_result_actual, total_result_diff