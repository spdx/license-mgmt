# Copyright 2022 Rohan Chandrashekar
# SPDX-License-Identifier:  MIT
'''Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'''


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
    path("About/",UserViews.aboutView, name="about"),
    path("Logout",UserViews.LogoutView, name="Logout"),
    path("logoutAndLicenseList",UserViews.logoutAndLicenseList, name="logoutAndLicenseList")
]