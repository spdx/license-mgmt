#package imports
from email.header import Header
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from django.contrib import messages
import csv
import datetime
import zipfile, os, io, requests

#model import
from user.models import *
from user.resources import licenseDataResource
from user.forms import *
from user.utilityFunctions import *
# Create your views here.

@login_required
def checkUser(request):    
    if request.user.is_superuser:
        return redirect("user:adminLogin")

    if request.user.groups.exists():
        role = ""
        if 'Uploader' in list(request.user.groups.values_list('name', flat = True)):
            role = "Uploader"
        if 'Approver' in list(request.user.groups.values_list('name', flat = True)):
            if role == "":
                role = "Approver"
            else:
                role = role +"AndApprover"
        if 'Publisher' in list(request.user.groups.values_list('name', flat = True)):
            if role == "":
                role = "Publisher"
            else:
                role = role +"AndPublisher"
        if 'Admin' in list(request.user.groups.values_list('name', flat = True)):
            if role == "":
                role = "Admin"
            else:
                role = role +"AndAdmin"
        request.session["role"] = role        
        messages.success(request, "Hey! Welcome back...")
        return redirect("user:dashboard")
    else:
        return render(request, "license_management_system/noRole.html")

@login_required
def headerReview(request):
    if "Publisher" in request.session['role']:  

        headerDetails = get_object_or_404(exportHeaderFields, user=request.user)       
        context = dict()
        context["context"]  = "Licenses Export: "
        context["secondaryContext"] = "Header Review"
        context["review"] = True

        if request.method == 'POST':
            form = ExportHeaderForm(request.POST or None, instance = headerDetails) 
            if form.is_valid():
                statusUpdate = request.POST.get("action") == "update"
                statusExport = request.POST.get("action") == "export"
                user = request.user
                if statusUpdate and not statusExport:
                    saveHeaderInfo(form, user)
                    HeaderInfo = exportHeaderFields.objects.get(user = request.user)   
                else:
                    HeaderInfo = form.save(commit = False)
                
                if request.session["Option"] == "zip":
                    return exportAndZip(request, HeaderInfo)
                else:
                    return export(request, HeaderInfo)
            else:
                context['form'] = form
                return render(request, "user/setHeaderDetails.html", context)  
        else:
            form = ExportHeaderForm(instance = headerDetails)           
            context["form"] = form
            return render(request, "user/setHeaderDetails.html", context)
    else:
        return render(request, "user/wrongUser.html")  
