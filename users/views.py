from datetime import date
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView


from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserChangeForm
from .models import EmailActivation, User

def register_done_view(request):
    return render(request, 'users/register_done.html')

def index_view(request):
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
    return render(request, 'users/index.html', {'form': form})

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

def profile_view(request):
    user = request.user
    days_since_joined = (timezone.now().date() - user.date_joined.date()).days
    today = date.today()
    user_profile = getattr(user, 'userprofile', None)  

    return render(request, 'users/profile.html', {
        'user': user,
        'days_since_joined': days_since_joined,
        'today': today,
        'user_profile': user_profile,})

class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("register_done")

    def form_valid(self, form):
        user = form.save(commit=False) 
        user.set_password(form.cleaned_data["password1"])
        user.is_active = False  
        user.save() 

        activation = EmailActivation.objects.create(user=user)
        activation.send_email()
      
        return super().form_valid(form)
        

def activate_user_view(request, token: str):
    activation = EmailActivation.objects.get(token=token)
    activation.is_active = True
    activation.user.is_active = True
    activation.user.save()
    activation.save()

    return redirect('index')

def logout_view(request):
    logout(request)
    return redirect('index')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
