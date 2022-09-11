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


#packages import
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from user.models import licenseData, Status
from django.views import View
from django.contrib import messages

#files import
from .forms import CreateUserForm, UserAuthenticationForm
from .decorators import authenticatedUser


# Create your views here.
class displayApprovedLicenses(ListView):
    template_name = "user_sign_in/licenseList.html"
    model = licenseData

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        querySet = licenseData.objects.filter(status = Status.objects.get(status = "Approved"))
        context['licenses'] = querySet  
        context['context'] = 'License List'     
        return context     
    
    def post(self, request, *args, **kwargs):
        form = UserAuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("user:checkUser")
        else:
            return render(request, "user_sign_in/loginPage.html",{
                'form': form,
                'no_user': True
            })

class SingleLicenseView(View):
    def get(self, request, slug):
        licenseObject = licenseData.objects.get(id=slug)
        text = licenseObject.licenseData.split("\n")

        context = {
           "licenseObject" : licenseObject,
           "context" : "License Details",
           "text": text
        }
        return render(request, "user_sign_in/licenseDetails.html", context)   

@authenticatedUser
def signin(request):
    form = UserAuthenticationForm()
    if request.method == 'POST':
        form = UserAuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("user:checkUser")
        else:
            return render(request, "user_sign_in/loginPage.html",{
                'form': form,
                'no_user': True
            })

    return render(request, "user_sign_in/loginPage.html",{
        'form': form,
        'no_user': False
    })

@authenticatedUser
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            #log the user in
            return redirect("user_sign_in:sign_in")
            
    context = {
        'form' : form
    }

    return render(request, 'user_sign_in/register.html', context)
  
@login_required
def error_404_view(request, exception):
    return render(request, 'license_management_system/404.html')