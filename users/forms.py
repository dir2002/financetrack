from django import forms
from django.forms import TextInput, PasswordInput, NumberInput, FileInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Имя', 'class': 'form-control'})    )
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'form-control'})    )
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер мобильного телефона', 'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Уникальный псевдоним', 'class': 'form-control'}))
    email = forms.EmailField(widget=TextInput(attrs={'placeholder': 'Адрес электронной почты', 'class': 'form-control'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'form-control'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Подтвердите пароль', 'class': 'form-control'}))
    avatar = forms.ImageField(required=False, widget=FileInput(attrs={'class': 'form-control'}))
    
    class Meta():
        model = User
        fields = ['email', 'password1', 'password2',
            'first_name', 'last_name', 'username', 'phone_number', 'avatar']
        
class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Электронный адрес', 'class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control'}))


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone_number', 'avatar']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)