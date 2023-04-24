from django.urls import path, include
from . import views, forms
import django.contrib.auth.views as auth_views

urlpatterns = [
    path('feedback', views.feedback_view, name='feedback'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/password_reset', auth_views.PasswordResetView.as_view(form_class=forms.CustomPasswordResetForm), name='password_reset'),
    path("accounts/", include("django.contrib.auth.urls"))
]
