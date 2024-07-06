# accounts/urls.py

from django.urls import path
from . import views, viewsAdmin, viewsStaff, viewsUser
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('accounts/login/', views.login_view, name='login'),
    path('', views.login_view, name='login'), 
    # path('register', views.signup_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    #Reset Password
    path('accounts/password/reset/', CustomPasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('accounts/reset/password/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
     #User
    path('dashboard/user', viewsUser.user, name='dashboard_user'),
    #Admin
    path('dashboard/admin', viewsAdmin.admin, name='dashboard_admin'),
    #Pelanggan
    path('dashboard/staff', viewsStaff.staff, name='dashboard_staff'),
    path('dashboard/staff/assets', viewsStaff.create_aset, name='add_assets'),
    path('dashboard/profile/', viewsStaff.dashboard_profile, name='profile'),
    path('dashboard/profile/update', viewsStaff.update_profile, name='update_profile'),
    path('dashboard/staff/assets-list', viewsStaff.list_aset, name='list_aset'),

    path('edit_asset/<int:asset_id>/', viewsStaff.edit_asset, name='edit_asset'),
    path('delete_asset/<int:asset_id>/', viewsStaff.delete_asset, name='delete_asset'),

    path('dashboard/kategori/add/', viewsStaff.tambah_kategori, name='tambah_kategori'),
    path('dashboard/posisi/add', viewsStaff.tambah_posisi, name='tambah_posisi'),
    path('dashboard/kategori/', viewsStaff.list_kategori, name='list_kategori'),
    path('dashboard/posisi/', viewsStaff.list_posisi, name='list_posisi'),

    path('dashboard/kategori/edit/<int:kategori_id>/', viewsStaff.edit_kategori, name='edit_kategori'),
    path('dashboard/posisi/edit/<int:posisi_id>/', viewsStaff.edit_lokasi, name='edit_lokasi'),


    path('delete_kategori/<int:kategori_id>/', viewsStaff.delete_kategori, name='delete_kategori'),
    path('delete_posisi/<int:posisi_id>/', viewsStaff.delete_posisi, name='delete_lokasi'),

    path('asset/<int:asset_id>/', viewsStaff.asset_detail, name='asset_detail'),

    path('asset/scan/<int:asset_id>/', viewsStaff.asset_scan_detail, name='asset_scan_detail'),

    path('export', viewsStaff.export_data, name='export_aset_baru'),
    path('export/posisi/', viewsStaff.export_posisi_asset, name='export_posisi_asset'),

    path('export/view/', viewsStaff.view_data, name='view_data'),
    path('export/view/posisi/', viewsStaff.view_posisi_asset, name='view_posisi'),
   


]

