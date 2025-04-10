from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages

from .forms import CustomUserCreationForm
from .models import EmailActivation

def register_done(request):
    return render(request, 'users/register_done.html')

def index(request):
    return render(request, 'users/index.html')


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
    
    

def activate_user(request, token: str):
    activation = EmailActivation.objects.get(token=token)
    activation.is_active = True
    activation.user.is_active = True
    activation.user.save()
    activation.save()

    return redirect('index')