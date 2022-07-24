"""SPDX_license_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from user_sign_in.forms import NewPasswordResetForm

urlpatterns = [
    path('superuser/', admin.site.urls),
    path("",include("user_sign_in.urls", namespace="user_sign_in"), name="user_sign_in"),
    path("user/",include("user.urls", namespace="user"), name="user"),

    #password reset views
    
    path("forgotPassword", auth_views.PasswordResetView.as_view(form_class = NewPasswordResetForm, template_name = 'user_sign_in/forgotPasswordPage.html'), name='forgot_password'),
       path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="user_sign_in/ResetLinkSent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="user_sign_in/forgotPasswordPage.html"), name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="user_sign_in/forgotPasswordPage.html"), 
        name="password_reset_complete"),
]
