from django.http import HttpResponse
from django.shortcuts import redirect

def authenticatedUser(viewFunction):
    def wrapperFunction(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("user:checkUser")
        else:
            return viewFunction(request, *args, **kwargs)
    
    return wrapperFunction