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

<<<<<<< Updated upstream:Source Code/user/views/commonViews.py
   
def export(request, slug):
    licenseResource = licenseDataResource()
    dataset = licenseResource.export()
    if slug == "csv":
        response = HttpResponse(dataset.csv, content_type = "text/csv")
        response['Content-Disposition'] = 'attachment; filename=License List' + str(datetime.datetime.now()) + \
            '.csv'
    elif slug == "json":
        response = HttpResponse(dataset.json, content_type = "application/json")
        response['Content-Disposition'] = 'attachment; filename=License List' + str(datetime.datetime.now()) + \
            '.json'
    elif slug == "xls":
        response = HttpResponse(dataset.xls, content_type = "application/vnd.ms=excel")
        response['Content-Disposition'] = 'attachment; filename=License List' + str(datetime.datetime.now()) + \
            '.xls'
=======
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
                return export(request, HeaderInfo)
            else:
                context['form'] = form
                return render(request, "user/setHeaderDetails.html", context)  
        else:
            form = ExportHeaderForm(instance = headerDetails)           
            context["form"] = form
            return render(request, "user/setHeaderDetails.html", context)
>>>>>>> Stashed changes:user/views/commonViews.py
    else:
        resource = None
    return response

def zipAndExport(request, slug):
    # response = HttpResponse(content_type='application/zip')
    # zip_file = zipfile.ZipFile(response, 'w')
    # zip_file.write()
    # response['Content-Disposition'] = 'attachment; filename={}'.format(str(datetime.datetime.now()))
    return render(request, "license_management_system/underMaintainance.html")
