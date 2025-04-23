from datetime import date
from django.http import HttpRequest
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
import logging


from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserChangeForm
from .models import EmailActivation, User
from transactions.models import Category
from transactions.utils import get_opening_balance_context, calculate_cash_balance, calculate_deposit_balance, calculate_invest_balance, calculate_long_debt_balance, calculate_short_debt_balance
from budget.utils import calculate_total_incomes, calculate_total_expenses, calculate_total_result
from transactions.forms import TransactionForm

logger = logging.getLogger('django')

def register_done_view(request):
    return render(request, 'users/register_done.html')

def oficial_doc_view(request):
    return render(request, 'users/documentation.html')

# представление главной страницы
def index_view(request):
    logger.info("Открыта страница входа") 
    if request.method == 'POST':
        logger.debug("Получен POST-запрос на аутентификацию")
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user and user.is_active:
                logger.info(f"Успешный вход: {email}")
                login(request, user)
                return redirect('profile')
            else:
                logger.warning(f"Ошибка входа: {email} — Неверные данные или аккаунт отключен")
                return redirect('login_error')
        else:
            logger.warning("Форма входа не прошла проверку")
            return redirect('login_error')
    else:
        logger.debug("Открыта форма входа")     
        form = CustomUserLoginForm()
    return render(request, 'users/index.html', {'form': form})

# представление ошибки входа
def login_error_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('profile')
            else:
                return redirect('login_error')
        else:
                return redirect('login_error')
    else:     
        form = CustomUserLoginForm()
    return render(request, 'users/login_error.html', {'form': form})

# Хендлер для обработки транзакции
def handle_transaction(request):
    form = TransactionForm(request.POST or None)
    logger.info("Обработка POST-запроса на транзакцию началась")
    if request.method == "POST" and form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        (f"Транзакция успешно сохранена для пользователя {request.user}")
        return TransactionForm()  
    return form 

# представление для профиля
@login_required
def profile_view(request):
    user = request.user
    logger.info(f"Профиль открыт: {user.username}")
    
    days_since_joined = (timezone.now().date() - user.date_joined.date()).days
    today = date.today()
    user_profile = getattr(user, 'userprofile', None)
    categories = Category.objects.prefetch_related('subcategories').all()
    user_task_count = request.user.tasks.count()

    form = handle_transaction(request)

    user_level = (
        'Транжира' if days_since_joined <= 3 else
        'Финансовый теоретик' if days_since_joined <= 10 else
        'Коммерсант' if days_since_joined <= 20 else
        'Финансовый гуру'
    )
    try:
        total_cash = calculate_cash_balance(request.user)
        total_deposit = calculate_deposit_balance(request.user)
        total_invest = calculate_invest_balance(request.user)
        total_long_debt = calculate_long_debt_balance(request.user)
        total_short_debt = calculate_short_debt_balance(request.user)
        total_incomes = calculate_total_incomes(request.user)
        total_expenses = calculate_total_expenses(request.user)
        total_result = calculate_total_result(request.user)
    except Exception as e:
        logger.error(f"Ошибка при вычислении баланса: {e}")


    context = {'user': user,
        'days_since_joined': days_since_joined,
        'today': today,
        'user_profile': user_profile,
        'user_level': user_level,
        "form": form,
        'categories': categories,
        'total_cash': total_cash,
        'total_deposit': total_deposit,
        'total_invest': total_invest,
        'total_long_debt': total_long_debt,
        'total_short_debt': total_short_debt,
        'total_incomes': total_incomes,
        'total_expenses': total_expenses,
        'total_result': total_result,
        'user_task_count': user_task_count
    }

    context.update(get_opening_balance_context(user))
    return render(request, 'users/profile.html', context)

# представление для регистрации пользователя
class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("register_done")

    def form_valid(self, form):
        try:
            user = form.save(commit=False) 
            user.set_password(form.cleaned_data["password1"])
            user.is_active = False  
            user.save()
            logger.info(f"Пользователь зарегистрирован: {user.username} (не активен)") 

            activation = EmailActivation.objects.create(user=user)
            activation.send_email()
            logger.info(f"Активационное письмо отправлено пользователю: {user.username}")
        except Exception as e:
            logger.error(f"Ошибка при регистрации пользователя: {e}")
        return super().form_valid(form)
        
# представление для активации пользователя
def activate_user_view(request, token: str):
    activation = EmailActivation.objects.get(token=token)
    activation.is_active = True
    activation.user.is_active = True
    activation.user.save()
    activation.save()

    return redirect('index')

# представление для выхода из аккаунта
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

# представление для обновления профиля
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        user = self.request.user
        try:
            logger.info(f"Пользователь {user.username} обновляет профиль.")
            response = super().form_valid(form)
            logger.info(f"Профиль пользователя {user.username} успешно обновлён.")
            return response
        except Exception as e:
            logger.error(f"Ошибка при обновлении профиля пользователя {user.username}: {e}", exc_info=True)
            return super().form_invalid(form)

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('index')
    template_name = 'users/profile_delete.html'

    def get_object(self, queryset=None):
        return self.request.user