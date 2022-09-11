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
<<<<<<< Updated upstream:Source Code/user_sign_in/urls.py
from django.contrib import admin
from django.urls import path
from . import views
=======
from re import template
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from user_sign_in.forms import NewPasswordResetForm
>>>>>>> Stashed changes:SPDX_license_management_system/urls.py

urlpatterns = [
<<<<<<< Updated upstream:Source Code/user_sign_in/urls.py
    path("",views.displayApprovedLicenses.as_view(), name="displayApprovedLicenses"),
    path("licenseView/<int:slug>", views.SingleLicenseView.as_view(),
         name="licenseDetailsPage"),    
    path("signIn",views.signin, name="sign_in"),
    path("forgotPassword", views.forgot_password, name='forgot_password'),
    path("register",views.register, name="register"),
]
=======
    path('superuser/', admin.site.urls),
    path("",include("user_sign_in.urls", namespace="user_sign_in"), name="user_sign_in"),
    path("user/",include("user.urls", namespace="user"), name="user")
]
>>>>>>> Stashed changes:SPDX_license_management_system/urls.py
