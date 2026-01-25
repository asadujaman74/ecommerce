from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [

    path('register/', views.register, name = 'register'),

    # register email verfication flow URLs

    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name = 'email-verification'),

    path('email-verification-sent/', views.email_verification_sent, name = 'email-verification-sent'),

    path('email-verification-success/', views.email_verification_success, name = 'email-verification-success'),

    path('email-verification-failed/', views.email_verification_failed, name = 'email-verification-failed'),

    # Login / Logout URLs

    path('login/', views.my_login , name='my-login'),
    path('user-logout/', views.user_logout , name='user-logout'),

    # dashboard / Profile URLs

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile-management/', views.profile_management, name='profile-management'),
    path('delete-account/', views.delete_account, name='delete-account'),

    # Password management URLs

    # Submit your email form
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = 'account/password-reset/password-reset.html'), name = 'reset_password'),

    # Success Message Stating that a password reset email sent
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'account/password-reset/password-reset-sent.html'), name = 'password_reset_done'),

    # Password reset token send in mail
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'account/password-reset/password-reset-form.html'), name = 'password_reset_confirm'),

    # Password reset Success 
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'account/password-reset/password-reset-complete.html'), name = 'password_reset_complete'),


    # Shipping Management
    
    path('manage-shipping/', views.manage_shipping, name='manage-shipping'),
    


]