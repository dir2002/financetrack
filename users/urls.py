from django.urls import path, include
from .views import index, register_done, RegisterView, activate_user
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/done/', register_done, name='register_done'),
    path('users/activate/<str:token>/', activate_user, name='activate'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

]
