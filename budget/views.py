import logging
from datetime import date
from django.db import IntegrityError
from django.utils import timezone
from django.forms import  DecimalField, ValidationError, modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Sum, F, Value, DecimalField, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.db.models import OuterRef, Subquery


from .models import BudgetLimit
from .forms import BudgetLimitForm, BudgetLimitUpdateForm
from transactions.models import Category, SubCategory, Transaction

logger = logging.getLogger('django')


# представления для CRUD операций по статьям
@login_required
def create_limits_view(request):
    user = request.user
    BudgetLimitFormSet = modelformset_factory(BudgetLimit, form=BudgetLimitForm, extra=1, max_num=8)

    if request.method == "POST":
        formset = BudgetLimitFormSet(request.POST)

        for form in formset:
            form.empty_permitted = False

        if formset.is_valid():
            has_duplicates = False

            for form in formset:
                category = form.cleaned_data.get("category")
                subcategory = form.cleaned_data.get("subcategory")

                if BudgetLimit.objects.filter(user=user, category=category, subcategory=subcategory).exists():
                    form.add_error(None, f"Статья категории '{subcategory}' уже существует. Пожалуйста, обновите существующую статью.")
                    has_duplicates = True

            if not has_duplicates:
                limits = formset.save(commit=False)
                for limit in limits:
                    limit.user = user
                    limit.save()
                    logger.info(f"Создан лимит: {limit.category} — {limit.subcategory}")
                return redirect("limits_list")
            else:
                logger.info(f"Обнаружены дубликаты при создании лимитов пользователем {user.username}")
        else:
            logger.warning(f"Ошибки в форме лимитов: {formset.errors}")

    else:
        logger.info(f"Пользователь {user.username} открыл форму создания лимитов.")
        formset = BudgetLimitFormSet(queryset=BudgetLimit.objects.none())

    categories = Category.objects.prefetch_related("subcategories").all()
    return render(request, "budget/create_limits.html", {
        "formset": formset,
        "categories": categories
    })

class LimitUpdateView(LoginRequiredMixin, UpdateView):
    model = BudgetLimit
    form_class = BudgetLimitUpdateForm
    template_name = 'budget/limit_update.html'
    success_url = reverse_lazy('find_limit')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user  

        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "Лимит с такой категорией и подкатегорией уже существует. Проверьте свои данные и введите повторно.")
            return self.form_invalid(form)
    
class LimitDeleteView(LoginRequiredMixin, DeleteView):
    model = BudgetLimit
    form_class = BudgetLimitForm
    template_name = 'budget/limit_delete.html'
    success_url = reverse_lazy('find_limit')

    # добавляем обработчик POST-запроса для DeleteView
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs) 

@login_required
def limits_list_view(request):
    limits_list = BudgetLimit.objects.filter(user=request.user).order_by("id")

    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    min_amount = request.GET.get("min_limit_amount")
    max_amount = request.GET.get("max_limit_amount")
    search_query = request.GET.get("search")

    if category_id:
        limits_list = limits_list.filter(category_id=category_id)
    if subcategory_id:
        limits_list = limits_list.filter(subcategory_id=subcategory_id)
    if start_date:
        limits_list = limits_list.filter(end_date__gte=start_date)
    if end_date:
        limits_list = limits_list.filter(end_date__lte=end_date)
    if min_amount and min_amount.isdigit():
        limits_list = limits_list.filter(limit_amount__gte=int(min_amount))
    if max_amount and max_amount.isdigit():
        limits_list = limits_list.filter(limit_amount__lte=int(max_amount))
    if search_query:
        limits_list = limits_list.filter(category__name__icontains=search_query)

    paginator = Paginator(limits_list, 18)
    page_number = request.GET.get("page")  
    custom_limits = paginator.get_page(page_number)

    categories = Category.objects.prefetch_related('subcategories').all()

    return render(request, "budget/limits_list.html", {
        'limits': custom_limits,  
        'categories': categories,
        'start_date': request.GET.get("start_date", ""),  
        'end_date': request.GET.get("end_date", ""),
    })
# представление для поиска статьи
@login_required
def find_limit_view(request):
    limit = None  
    error_message = None  

    if request.method == "POST":
        limit_id = request.POST.get("limit_id")

        if not limit_id or not limit_id.isdigit():
            error_message = "Ошибка: Введите корректный ID статьи."
        else:
            limit = BudgetLimit.objects.filter(id=limit_id, user=request.user).first()
            if limit:
                return redirect("limit_update", pk=limit.id)  
            else:
                error_message = "Ошибка: Статья не найдена. Повторите попытку."

    return render(request, "budget/find_limit.html", {
        "error_message": error_message})

# представление для создания бюджета

@login_required
def create_budget_view(request):
    today = date.today()

    # 🔹 Определяем фильтр пользователя
    user_filter = Q(budgetlimit__user=request.user)
    transaction_filter = Q(transaction__user=request.user)

    # 🔹 Запрашиваем данные сразу с фильтрацией
    incomes_summary = SubCategory.objects.filter(category__pk=1).annotate(
    total_planned=Coalesce(Sum("budgetlimit__limit_amount", filter=user_filter, distinct=True), Value(0), output_field=DecimalField()),
    total_actual=Coalesce(Sum("transaction__amount", filter=transaction_filter), Value(0), output_field=DecimalField())
    )

    expenses_summary = SubCategory.objects.filter(category__pk=2).annotate(
        total_planned=Coalesce(Sum("budgetlimit__limit_amount", filter=user_filter, distinct=True), Value(0), output_field=DecimalField()),
        total_actual=Coalesce(Sum("transaction__amount", filter=transaction_filter), Value(0), output_field=DecimalField())
    )

    # 🔹 Агрегируем итоговые суммы
    total_incomes = incomes_summary.aggregate(
        total_planned_sum=Sum("total_planned"),
        total_actual_sum=Sum("total_actual"),
        total_diff_sum=F("total_planned_sum") - F("total_actual_sum")  # ✅ Считаем разницу сразу!
    )

    total_expenses = expenses_summary.aggregate(
        total_planned_sum=Sum("total_planned"),
        total_actual_sum=Sum("total_actual"),
        total_diff_sum=F("total_planned_sum") - F("total_actual_sum")
    )

    # 🔹 Проверяем, есть ли ошибки в данных
    if not total_incomes["total_planned_sum"] or not total_expenses["total_planned_sum"]:
        logger.warning("Некорректные данные в `total_incomes` или `total_expenses`")

    # 🔹 Убеждаемся, что `None` заменены на `0`
    total_result_planned = (total_incomes.get("total_planned_sum") or 0) - (total_expenses.get("total_planned_sum") or 0)
    total_result_actual = (total_incomes.get("total_actual_sum") or 0) - (total_expenses.get("total_actual_sum") or 0)
    total_result_diff = (total_incomes.get("total_diff_sum") or 0) - (total_expenses.get("total_diff_sum") or 0)

    return render(request, "budget/create_budget.html", {
        "today": today,
        "incomes_summary": incomes_summary,
        "total_incomes": total_incomes,
        "expenses_summary": expenses_summary,
        "total_expenses": total_expenses,
        "total_result_planned": total_result_planned,
        "total_result_actual": total_result_actual,
        "total_result_diff": total_result_diff
    })