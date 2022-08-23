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
from django.urls import path
from .views import commonViews, UserViews
from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
app_name = "user"
urlpatterns = [
    #common urls
    path("loadingDashboard",commonViews.checkUser, name="checkUser"),
    path("headerReview",commonViews.headerReview, name="headerReview"),

    #User urls
    path('', RedirectView.as_view(url=reverse_lazy('admin:index')), name="adminLogin"),
    path("Dashboard",UserViews.dashboard, name="dashboard"),
    path("Upload",UserViews.upload, name="upload"),
    path("viewLicenses/<slug:slug>",UserViews.searchLicensesView.as_view(), name="viewLicenses"),
    path("LicenseTracking/<int:slug>", UserViews.licenseTrackingView.as_view(), name="LicenseTracking"),
    path("LicenseEdit/<int:slug>", UserViews.LicenseEdit, name="licenseEdit"),
    path("LicenseView/<int:slug>", UserViews.SingleLicenseView.as_view(),name="licenseDetails"),
    path("LatestLicensesChanged", UserViews.trackViews.as_view(), name="TrackLatestLicenses"),
    path("Users/<slug:slug>",UserViews.userView.as_view(), name="users"),
    path("UserActivity,<int:slug>",UserViews.trackUserViews.as_view(), name="userActivity"),
    path("setNamespace",UserViews.setNamespace, name="namespace"),
    path("headerMaintainance",UserViews.headerMaintainance, name="headerMaintainance"),
    path("setGroups/<int:slug>",UserViews.setGroups, name="setGroups"),
    path("deactivateProfile/<int:slug>",UserViews.deactivateProfile, name="deactivateProfile"),
    path("Profile",UserViews.profile, name="profile"),
    path("Settings/",UserViews.settings, name="settings"),
    path("Logout",UserViews.LogoutView, name="Logout"),
    path("logoutAndLicenseList",UserViews.logoutAndLicenseList, name="logoutAndLicenseList")
]