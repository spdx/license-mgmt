"""license_management_system URL Configuration

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
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "user_sign_in"
urlpatterns = [
    path("",views.displayApprovedLicenses.as_view(), name="displayApprovedLicenses"),
    path("licenseView/<int:slug>", views.SingleLicenseView.as_view(),
         name="licenseDetailsPage"),    
    path("signIn",views.signin, name="signIn"),    
    path("register",views.register, name="register"),
]