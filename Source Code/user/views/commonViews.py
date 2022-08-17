#package imports
from django.shortcuts import redirect
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
from user.models import licenseData
from user.resources import licenseDataResource
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

   
def export(request):
    licenseResource = licenseDataResource()
    dataset = licenseResource.export()
    response = HttpResponse(dataset.json, content_type = "application/json")
    response['Content-Disposition'] = 'attachment; filename=License List' + str(datetime.datetime.now()) + \
        '.json'
    return response

def zipAndExport(request):
    # response = HttpResponse(content_type='application/zip')
    # zip_file = zipfile.ZipFile(response, 'w')
    # zip_file.write()
    # response['Content-Disposition'] = 'attachment; filename={}'.format(str(datetime.datetime.now()))
    return render(request, "license_management_system/underMaintainance.html")
