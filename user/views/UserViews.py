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
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from user_sign_in.models import User

#file imports
from user.decorators import allowedUsers
from user.forms import licenseForm
from user.utilityFunctions import licenseTrackingFunction, saveLicense, validityAndText, duplicateCheck
from user.models import Status, licenseData, licenseTracking, operationType, namespace
from user_sign_in.forms import modifyUserForm
# Create your views here.

#Uploader Specific Views
@login_required
def upload(request):
    if "Uploader" or "Admin" in request.session["role"]:
        form = licenseForm()

        context = {
            'form': form,
            "context": "Upload License",
            "textError": False,
            "duplicateText": False,
        }

        if request.method == 'POST':
            form = licenseForm(data = request.POST)
            if form.is_valid():
                name = form.cleaned_data["name"]

                licenseUploadField = request.FILES
                if len(licenseUploadField)!=0:
                    fileUploadText = licenseUploadField['licenseFile'].read().decode()
                else:
                    fileUploadText = None
                
                isWrongSelection, textField = validityAndText(form, fileUploadText)
                if isWrongSelection:
                    context["textError"] = True
                    return render(request, "user/upload.html", context)
                else:
                    isDuplicate = duplicateCheck(textField, name)
                    if isDuplicate[0]:
                        context["duplicateText"] = True
                        context["DuplicateLicense"] = isDuplicate[1]
                        return render(request, "user/upload.html", context)
                    else:
                        saveLicense(form, "draft", textField, isDuplicate[1])
                        licenseTrackingFunction(name, request.user, 'new', "New License")
                        messages.success(request, "License sent to approver successfully!")
                        if "Admin" in request.session["role"]:
                            return redirect("user:dashboard")
            else:
                context["form"] = form
                return render(request, "user/upload.html",context)
        return render(request, "user/upload.html", context)
    else:
        return render(request, "user/wrongUser.html")

@login_required
def LicenseEdit(request, slug):   
    licenseObject = get_object_or_404(licenseData, id=slug)
    form = licenseForm(request.POST or None, instance = licenseObject) 
    if "Uploader" or "Admin" in request.session["role"]:
        context = {
            'form': form,
            "context": "Edit License: ",
            "secondaryContext": licenseObject,
            "textError": False,
            "duplicateText": False,
        }

        if request.method == 'POST':
            if form.is_valid():
                name = form.cleaned_data["name"]

                licenseUploadField = request.FILES
                if len(licenseUploadField)!=0:
                    fileUploadText = licenseUploadField['licenseFile'].read().decode()
                else:
                    fileUploadText = None
                
                isWrongSelection, textField = validityAndText(form, fileUploadText)
                if isWrongSelection:
                    context["textError"] = True
                    return render(request, "user/upload.html", context)
                else:
                    isDuplicate = duplicateCheck(textField, name)
                    if isDuplicate[0]:
                        context["duplicateText"] = True
                        context["DuplicateLicense"] = isDuplicate[1]
                        return render(request, "user/upload.html", context)
                    else:
<<<<<<< Updated upstream:Source Code/user/views/UserViews.py
                        print("Hello", textField)
                        saveLicense(form, "draft", textField)
                        licenseTrackingFunction(name, request.user, 'new', "New License")
=======
                        saveLicense(form, "draft", textField, isDuplicate[1])
                        licenseTrackingFunction(name, request.user, 'modified', "New License")
>>>>>>> Stashed changes:user/views/UserViews.py
                        messages.success(request, "License sent to approver successfully!")
                        return redirect("user:dashboard")
                        
            else:
                context["form"] = form
                return render(request, "user/upload.html",context)
        return render(request, "user/upload.html", context)
    else:
        return render(request, "user/wrongUser.html")
    

# Common Views
@login_required
def dashboard(request):
    context = {
        "context":"Dashboard",
    }
    context["name"] = request.user
    try:
        pendingLicenses = licenseData.objects.filter(status = Status.objects.get(status="Draft")).count()   
    except:
        pendingLicenses = 0
    try:
        approvedLicenses = licenseData.objects.filter(status = Status.objects.get(status="Approved")).count() 
    except:
        approvedLicenses = 0
    try:
        rejectedLicenses = licenseData.objects.filter(status = Status.objects.get(status="Rejected")).count() 
    except:
        rejectedLicenses = 0
    try:
        uploadedLicenses = licenseData.objects.all().count()     
    except:
        uploadedLicenses = 0  
    contextObjects = licenseTracking.objects.exclude(date__lt = request.user.last_login)
    if "Admin" not in request.session["role"]:
        if "Uploader" not in request.session["role"]:
            contextObjects = contextObjects.filter(operationType = operationType.objects.get(operation = "New") and operationType.objects.get(operation = "Modified"))
        if "Approver" not in request.session["role"]:
            contextObjects = contextObjects.exclude(operationType = operationType.objects.get(operation = "Modified")).exclude(operationType = operationType.objects.get(operation = "New"))
    else:
        try:
            ApproverCount = User.objects.filter(groups__name__in = ["Approver"]).exclude(groups__name__in = ["Uploader"]).count()
        except:
            ApproverCount = 0
        context["ApproverCount"] = ApproverCount
        try:
            UploaderCount  =  User.objects.filter(groups__name__in = ["Uploader"]).exclude(groups__name__in = ["Approver"]).count()
        except:
            UploaderCount = 0
        context["UploaderCount"] = UploaderCount
        try:
            ApproverUploaderCount = User.objects.filter(groups__name__in = ["Approver"]).filter(groups__name__in = ["Uploader"]).count()
        except:
            ApproverUploaderCount = 0
        context["ApproverUploaderCount"] = ApproverUploaderCount
        try:
            AdminCount = User.objects.filter(groups__name__in = ["Admin"]).count()
        except:
            AdminCount = 0
        context["AdminCount"] = AdminCount 
        try:
            NoRoleCount = User.objects.exclude(groups__name__in = ["Approver","Uploader","Admin"]).exclude(is_superuser=True).count()
        except:
            NoRoleCount = 0
        context["NoRoleCount"] = NoRoleCount 
        try:
            totalUsers = User.objects.exclude(is_superuser=True).count()
        except:
            totalUsers = 0
        context["totalUsers"] = totalUsers 
    changeInLicenses = contextObjects.count() 
    context["pendingLicenses"] = pendingLicenses
    context["approvedLicenses"] = approvedLicenses
    context["rejectedLicenses"] = rejectedLicenses
    context["uploadedLicenses"] = uploadedLicenses
    context["changeInLicenses"] = changeInLicenses
    return render(request, "user/dashboard.html",context)

class searchLicensesView(LoginRequiredMixin, ListView):
    template_name = "user/searchLicenses.html"
    model = licenseData

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        querySet = licenseData.objects.all()
        slug = ""
        if self.kwargs.get('slug'):
            if self.kwargs['slug'] == "all":
                context['licenses'] = licenseData.objects.all() 
                slug = "Complete"
            elif self.kwargs['slug'] == "DraftorRejected":
                context['licenses'] = licenseData.objects.exclude(status = Status.objects.get(status = "Approved")) 
                slug = "Draft and Rejected"
            else:
                querySet = querySet.filter(status = Status.objects.get(status = self.kwargs['slug']))
                slug = self.kwargs['slug']
        context['licenses'] = querySet  
        context['context'] = '{} License List'.format(slug)     
        return context 
<<<<<<< Updated upstream:Source Code/user/views/UserViews.py
=======

    def post(self, request, *args, **kwargs):       
        if 'ApproverPOST' not in request.POST: 
            licenseList = list()
            for license in licenseData.objects.filter(status = Status.objects.get(status = "Approved")):
                searchLicense = "{}".format(license.id)
                if request.POST.get(searchLicense) != None:
                    licenseList.append(license.id)
            if len(licenseList) == 0:
                messages.warning(request, "Select atleast one License for export!")
                return redirect("user:viewLicenses", slug="Approved")
            request.session["list"] = licenseList
            return export(request)
        else:
            return exportAndZipApprover(request)

>>>>>>> Stashed changes:user/views/UserViews.py

class licenseTrackingView(LoginRequiredMixin, ListView):
    template_name = "user/licenseTracking.html"
    model = licenseTracking

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('slug'):
            licenseObject = licenseData.objects.get(id = self.kwargs['slug'])
        context['TrackingDetails'] = licenseTracking.objects.filter(license =licenseObject ).order_by("date")
        context['context'] = 'Life Cycle of the License:'
        context["secondaryContext"] = licenseObject
        return context

class trackViews(LoginRequiredMixin, ListView):
    template_name = "user/licenseTracking.html"
    model = licenseTracking

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contextObjects = licenseTracking.objects.exclude(date__lt = self.request.user.last_login)
        if "Admin" not in self.request.session["role"]:
            if "Uploader" not in self.request.session["role"]:
                contextObjects = contextObjects.filter(operationType = operationType.objects.get(operation = "New") and operationType.objects.get(operation = "Modified"))
            if "Approver" not in self.request.session["role"]:
                contextObjects = contextObjects.exclude(operationType = operationType.objects.get(operation = "Modified")).exclude(operationType = operationType.objects.get(operation = "New"))
        context['TrackingDetails'] = contextObjects
        context['context'] = 'Licenses with changes: '     
        context['secondaryContext'] = 'Since last login'  
        return context  

@login_required
<<<<<<< Updated upstream:Source Code/user/views/UserViews.py
def profile(request):
    form = modifyUserForm(request.POST or None, instance=request.user)
    context = {
        "form" : form,
        "context": "Edit your profile"
    }

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated!")
            return redirect("user:dashboard")


    return render(request, "user/userprofile.html", context)

@login_required
def settings(request):
    return render(request, "license_management_system/underMaintainance.html")

@login_required
def LogoutView(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logged Out Successfully!")
        return redirect("user_sign_in:displayApprovedLicenses")

    return render(request, 'user/logout.html')
=======
def headerMaintainance(request):
    if "Publisher" in request.session['role']:  

        headerDetails = get_object_or_404(exportHeaderFields, user=request.user)       
        context = dict()
        context["context"]  = "Licenses Export: "
        context["secondaryContext"] = "Header Maintainance"

        if request.method == 'POST':
            form = ExportHeaderForm(request.POST or None, instance = headerDetails) 
            if form.is_valid():
                user = request.user
                saveHeaderInfo(form, user)
                messages.success(request, "Header Info saved successfully!")
                return redirect("user:viewLicenses",slug="Approved")
            else:
                context['form'] = form
                return render(request, "user/setHeaderDetails.html", context)  
        form = ExportHeaderForm(instance = headerDetails)           
        context["form"] = form
        return render(request, "user/setHeaderDetails.html", context)
    else:
        return render(request, "user/wrongUser.html")
>>>>>>> Stashed changes:user/views/UserViews.py

#approver Specific view
class SingleLicenseView(LoginRequiredMixin, View):
    def get(self, request, slug):
        licenseObject = licenseData.objects.get(id=slug)
        text = licenseObject.licenseData.split("\n")
        latestComments = licenseTracking.objects.filter(license = licenseObject).order_by("-date")[0]
        context = {
           "licenseObject" : licenseObject,
           "context" : "Details of the License",
           "secondaryContext" : licenseObject,
           "latestComments": latestComments,
           "text": text
        }  
        if licenseObject.status == Status.objects.get(status = "Draft"):
            context["isDraft"] = True
        else:
            context["isDraft"] = False
        return render(request, "user/licenseDetails.html", context)  
    
    def post(self, request, slug):
        statusAccept = self.request.POST.get("action") == "accept"
        statusReject = self.request.POST.get("action") == "reject"
        statusDelete = self.request.POST.get("action") == "delete"
        licenseObject = get_object_or_404(licenseData, id=slug)
        name = licenseObject.name
        if statusDelete:
            licenseObject.delete()
            messages.success(request, "License {} Deleted".format(name))
            return redirect("user:viewLicenses", slug="all")
        comment = self.request.POST.get('Comments')
        if comment is None:
            comment = "--No comments given--"
        if statusAccept and not statusReject:
            statusObject = Status.objects.get(status = "Approved")            
            licenseTrackingFunction(name, request.user, 'approved', comment)            
        else:
            statusObject = Status.objects.get(status = "Rejected")            
            licenseTrackingFunction(name, request.user, 'rejected', comment)
        licenseObject.status = statusObject
        licenseObject.save()
        messages.success(request, "Saved Successfully!")
        return redirect("user:viewLicenses", slug="all") 

#admin specific views

class userView(LoginRequiredMixin, ListView):
    template_name = "user/userList.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        condition =  self.kwargs.get('slug')
        if condition == "Approver" or condition == "Uploader" or condition == "Admin":
            if condition == "Approver":
                context['Users'] = User.objects.filter(groups__name__in = [condition]).exclude(groups__name__in = ["Uploader"])
            elif condition == "Uploader":
                context['Users'] = User.objects.filter(groups__name__in = [condition]).exclude(groups__name__in = ["Approver"])
            else:
                context['Users'] = User.objects.filter(groups__name__in = [condition])
            context['context'] = '{} List'.format(condition)
        elif condition == "ApproverAndUploader":
            context['Users'] = User.objects.filter(groups__name__in = ["Approver"]).filter(groups__name__in = ["Uploader"])
            context['context'] = 'List of Users with roles Of'
            context['secondaryContext'] = ' both Approver and Uploader'
        elif condition == 'NewUsers':
            context['Users'] = User.objects.exclude(groups__name__in = ["Approver","Uploader","Admin"]).exclude(is_superuser=True)
            context['context'] = 'List of Users with '
            context['secondaryContext'] = ' no roles'
        elif condition == 'All':
            context['Users'] = User.objects.exclude(is_superuser=True)
            context['context'] = 'List of all Users'
        else:
            context['context'] = 'Oops! '
            context['secondaryContext'] = ' No such table.'
        return context

class trackUserViews(LoginRequiredMixin, ListView):
    template_name = "user/licenseTracking.html"
    model = licenseTracking
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contextObjects = licenseTracking.objects.filter(user = User.objects.get(id = self.kwargs.get('slug')))
        context['TrackingDetails'] = contextObjects
        context['context'] = 'Activity of User: '     
        context['secondaryContext'] = User.objects.get(id = self.kwargs.get('slug'))
        return context 

@login_required
def deactivateProfile(request, slug):
    if "Admin" in request.session["role"]: 
        userObject = User.objects.get(id = slug)
        context = {
            "name": userObject,
            "context": "Profile Management",
            "noSelection": False
        } 

        if userObject.is_active:
            context["profileDeaactivated"] = False
        else:
            context["profileDeaactivated"] = True        
        if request.method == "POST":   
            if request.POST.get("action") != None:
                if userObject.is_active:
                    userObject.is_active = False
                    userObject.save()
                    messages.success(request, 'Profile successfully disabled.')
                else:
                    userObject.is_active = True
                    userObject.save()
                    messages.success(request, 'Profile successfully enabled')            
                return redirect("user:dashboard")
            else:
                context["noSelection"] = True        
        return render(request, "user/deactivateProfile.html", context)
    else:
        return render(request, "user/wrongUser.html")

@login_required
def setNamespace(request):   
    if "Admin" in request.session["role"]:
        try:
            namespaceObject = namespace.objects.all()[0]
        except IndexError:
            namespaceObject = None
        if namespaceObject == None:
            context ={
                "text": "",
                "context": "Set Namespace"
            }
        else:
            context ={
                "text": namespaceObject.namespaceText,
                "context": "Set Namespace"
            }

        if request.method=="POST":
            if namespaceObject == None:
                newnamespace = namespace.objects.create(
                    namespaceText = request.POST.get("namespace")
                )
                newnamespace.save()
                messages.success(request, "Namespace created Successfully!")
            else:
                newnamespace = namespace.objects.get(id = namespaceObject.id)
                newnamespace.namespaceText = request.POST.get("namespace")
                newnamespace.save()
                messages.success(request, "Namespace Editted successfully!")
            
            return redirect("user:dashboard")

        return render(request, "user/namespace.html", context)   
    else:
        return render(request, "user/wrongUser.html")

@login_required
def setGroups(request, slug):
    userObject = User.objects.get(id = slug)
    context = {
        "name": userObject,
        "context": "Roles",
        "isApprover": False,
        "isUploader": False,
        "isAdmin": False,
        "wrongSelection": False,
        "noSelection": False
    }
    if userObject.groups.exists():
        if "Approver" in list(userObject.groups.values_list('name', flat = True)): 
            context["isApprover"] = True
        if "Uploader" in list(userObject.groups.values_list('name', flat = True)): 
            context["isUploader"] = True
        if "Admin" in list(userObject.groups.values_list('name', flat = True)): 
            context["isAdmin"] = True

    if request.method=="POST":
        if request.POST.get("Admin") != None:
            if request.POST.get("Uploader") == None and request.POST.get("Approver") == None:
                userObject.groups.clear()
                groupObject = Group.objects.get(name = "Admin")
                userObject.groups.add(groupObject)
                messages.success(request, "Role added successfully!")
                return redirect("user:users")
            else:
                context["wrongSelection"] = True
        elif request.POST.get("Uploader") != None or request.POST.get("Approver") != None:            
            userObject.groups.clear()
            if request.POST.get("Approver") != None:
                groupObject = Group.objects.get(name = "Approver")
                userObject.groups.add(groupObject)
            if request.POST.get("Uploader") != None:
                groupObject = Group.objects.get(name = "Uploader")
                userObject.groups.add(groupObject)
            messages.success(request, "Role added successfully!")
            return redirect("user:dashboard")
        else:
            context["noSelection"] = True
    return render(request, "user/setGroups.html",context)

#General Views
@login_required
def profile(request):
    form = modifyUserForm(request.POST or None, instance=request.user)
    context = {
        "form" : form,
        "context": "Edit your profile"
    }

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated!")
            return redirect("user:dashboard")


    return render(request, "user/userprofile.html", context)

@login_required
def settings(request):
    return render(request, "license_management_system/underMaintainance.html")

@login_required
def LogoutView(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logged Out Successfully!")
        return redirect("user_sign_in:displayApprovedLicenses")

    return render(request, 'user/logout.html')

@login_required
def aboutView(request):
    context = {
        "context" : "About this application"
    }
    return render(request, 'user/about.html', context)


@login_required
def logoutAndLicenseList(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect("user_sign_in:displayApprovedLicenses")

    