from django.http import HttpResponse
from django.shortcuts import redirect

def allowedUsers(allowedRoles = []):
    def decorator(viewFunction):
        def wrapperFunction(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowedRoles:
                return viewFunction(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapperFunction        
    return decorator