from django.urls import path, include
from .views import index_view, register_done_view, RegisterView, ProfileUpdateView, activate_user_view, login_error_view, profile_view, logout_view
from django.contrib.auth import views as auth_views
from  django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView



urlpatterns = [
    path('', index_view, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/done/', register_done_view, name='register_done'),
    path('logout/', logout_view, name='logout'),
    path('login-error/', login_error_view, name='login_error'),
    path('profile/', profile_view, name='profile'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('users/activate/<str:token>/', activate_user_view, name='activate'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path ('password/', PasswordChangeView.as_view(template_name='users/password_change_form.html', success_url='password_change_done'), name='password_change'),
    path('password_change/success/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    
]
