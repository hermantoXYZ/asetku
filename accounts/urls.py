# accounts/urls.py

from django.urls import path
from . import views, viewsAdmin, viewsStaff, viewsUser
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('register', views.signup_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    #Reset Password
    path('accounts/password/reset/', CustomPasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('accounts/reset/password/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    #Admin
    path('dashboard/admin', viewsAdmin.admin, name='dashboard_admin'),
    #Pelanggan
    path('dashboard/staff', viewsStaff.staff, name='dashboard_staff'),
    #User
    path('dashboard/user', viewsUser.user, name='dashboard_user'),



]

