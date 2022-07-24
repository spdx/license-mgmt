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
def forgot_password(request):
    return render(request, 'user_sign_in/forgotPasswordPage.html',{
                "title" : "Forgot-password"
    })

@authenticatedUser
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Accounted created!")
            return redirect("user_sign_in:signIn")
            
    context = {
        'form' : form
    }

    return render(request, 'user_sign_in/register.html', context)
  
@login_required
def error_404_view(request, exception):
    return render(request, 'license_management_system/404.html')