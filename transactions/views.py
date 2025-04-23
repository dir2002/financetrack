import logging
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import  redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.core.paginator import Paginator


from .models import Transaction, Category, OpeningBalance
from .forms import TransactionForm, OpeningBalanceForm, TransactionUpdateForm
from users.models import User

logger = logging.getLogger('django')
# представление transaction_create_view для одновременного создания нескольких транзакций
@login_required
def transaction_create_view(request):
    TransactionFormSet = modelformset_factory(Transaction, form=TransactionForm, extra=1, max_num=8)

    if request.method == "POST":
        logger.info(f"Пользователь {request.user.username} отправил форму создания транзакций.")
        formset = TransactionFormSet(request.POST)

        for form in formset:
            form.empty_permitted = False  

        if formset.is_valid():
            try:
                transactions = formset.save(commit=False)
                for transaction in transactions:
                    transaction.user = request.user  
                    transaction.save()
                    logger.info(f"Создана транзакция ID {transaction.id} пользователем {request.user.username}.")
                return redirect('profile')  
            except Exception as e:
                logger.error(f"Ошибка при сохранении транзакции пользователя {request.user.username}: {e}", exc_info=True)
        else:
            logger.warning(f"Форма транзакции пользователя {request.user.username} содержит ошибки: {formset.errors}")

    else:
        formset = TransactionFormSet(queryset=Transaction.objects.none())

    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, "transactions/create_transaction_set.html", {"formset": formset, "categories": categories})

# представление transaction_profile_create_view для рендеринга формы создания транзакции на profile.html
@login_required
def transaction_profile_create_view(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user or User.objects.get(pk=29)
            transaction.save()
            
        else:
            print(form.errors)

    else:
        form = TransactionForm()

    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, "users/profile.html", {"form": form, "categories": categories})

# представление BalanceUpdateView для редактирования первоначального баланса остатков
class BalanceUpdateView(LoginRequiredMixin, UpdateView):
    model = OpeningBalance
    form_class = OpeningBalanceForm
    template_name = 'transactions/openning_balance_update.html'
    success_url = reverse_lazy('profile_update')

    def get_object(self):
        user = self.request.user
        logger.info(f"Пользователь {user.username} открывает форму редактирования баланса.")
        return OpeningBalance.objects.get(user=user)

    def form_valid(self, form):
        user = self.request.user
        try:
            # Обнуляем поля, если они пустые
            form.instance.cash_start_saldo = form.instance.cash_start_saldo or 0
            form.instance.deposit_start_saldo = form.instance.deposit_start_saldo or 0
            form.instance.investment_start_saldo = form.instance.investment_start_saldo or 0
            form.instance.short_debt_start_saldo = form.instance.short_debt_start_saldo or 0
            form.instance.long_debt_start_saldo = form.instance.long_debt_start_saldo or 0

            form.instance.user = user
            form.instance.date_saldo_update = timezone.now()

            logger.info(f"Пользователь {user.username} обновил стартовые балансы.")
            return super().form_valid(form)
        except Exception as e:
            logger.error(f"Ошибка при обновлении баланса пользователем {user.username}: {e}", exc_info=True)
            raise
    
# представления для редактирования транзакций 
@login_required
def find_transaction_view(request):
    transaction = None  
    error_message = None 

    if request.method == "POST":
        transaction_id = request.POST.get("transaction_id")

        if not transaction_id or not transaction_id.isdigit():
            error_message = "Ошибка: Введите корректный номер транзакции."
        else:
            transaction = Transaction.objects.filter(id=transaction_id, user=request.user).first()
            if transaction:
                return redirect("transaction_update", pk=transaction.id)
            else:
                error_message = "Ошибка: Транзакция не найдена. Повторите попытку."

    return render(request, "transactions/find_transaction.html", {
        "error_message": error_message})

class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionUpdateForm
    template_name = 'transactions/transaction_update.html'
    success_url = reverse_lazy('find_transaction')

class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    form_class = TransactionUpdateForm
    template_name = 'transactions/transaction_delete.html'
    success_url = reverse_lazy('find_transaction')

    # добавляем обработчик POST-запроса для DeleteView
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs) 

# представление для отображения списка транзакций и фильтрации
@login_required
def transactions_list_view(request):
    transactions_list = Transaction.objects.filter(user=request.user).order_by("id")

    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    min_amount = request.GET.get("min_amount")
    max_amount = request.GET.get("max_amount")
    search_query = request.GET.get("search")

    if category_id:
        transactions_list = transactions_list.filter(category_id=category_id)
    if subcategory_id:
        transactions_list = transactions_list.filter(subcategory_id=subcategory_id)
    if start_date:
        transactions_list = transactions_list.filter(date__gte=start_date)
    if end_date:
        transactions_list = transactions_list.filter(date__lte=end_date)
    if min_amount and min_amount.isdigit():
        transactions_list = transactions_list.filter(amount__gte=int(min_amount))
    if max_amount and max_amount.isdigit():
        transactions_list = transactions_list.filter(amount__lte=int(max_amount))
    if search_query:
        transactions_list = transactions_list.filter(description__icontains=search_query)

    paginator = Paginator(transactions_list, 18)
    page_number = request.GET.get("page") 
    custom_transactions = paginator.get_page(page_number)

    categories = Category.objects.prefetch_related('subcategories').all()

    return render(request, "transactions/transactions_list.html", {
        'transactions': custom_transactions,  
        'categories': categories,
        'start_date': request.GET.get("start_date", ""), 
        'end_date': request.GET.get("end_date", ""),
    })