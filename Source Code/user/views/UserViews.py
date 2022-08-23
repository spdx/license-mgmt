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
from user.forms import licenseForm, ExportHeaderForm
from user.utilityFunctions import *
from user.models import *
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
                    if duplicateCheck(textField, name):
                        context["duplicateText"] = True
                        return render(request, "user/upload.html", context)
                    else:
                        print("Hello", textField)
                        saveLicense(form, "draft", textField)
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
                    if duplicateCheck(textField, name):
                        context["duplicateText"] = True
                        return render(request, "user/upload.html", context)
                    else:
                        saveLicense(form, "draft", textField)
                        licenseTrackingFunction(name, request.user, 'modified', "New License")
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
    pendingLicenses, approvedLicenses, rejectedLicenses, uploadedLicenses = dashboardOverallStats()
    contextObjects = licenseTracking.objects.exclude(date__lt = request.user.last_login)

    #Publisher only role
    context["onlyPublisher"] = False
    if request.session["role"] == "Publisher":
        contextObjects=contextObjects.filter(operationType = operationType.objects.get(operation = "Approved"))
        context["onlyPublisher"]  = True

    if "Admin" not in request.session["role"]:
        if "Uploader" not in request.session["role"]:
            contextObjects = contextObjects.filter(operationType = operationType.objects.get(operation = "New") and operationType.objects.get(operation = "Modified"))
        if "Approver" not in request.session["role"]:
            contextObjects = contextObjects.exclude(operationType = operationType.objects.get(operation = "Modified")).exclude(operationType = operationType.objects.get(operation = "New"))
        LicenseStatus, LicenseStatusCount = getChartsDetails(request)
        context["var"] = LicenseStatus
        context["val"] = LicenseStatusCount
    else:
        NoRoleCount, AdminCount, ApproverUploaderCount, UploaderPublisherCount, ApproverPublisherCount, UploaderCount, ApproverCount, PublisherCount, totalUsers = UserCount(User)
        context["NoRoleCount"] = NoRoleCount 
        context["AdminCount"] = AdminCount
        context["ApproverUploaderCount"] = ApproverUploaderCount
        context["UploaderPublisherCount"] = UploaderPublisherCount
        context["ApproverPublisherCount"] = ApproverPublisherCount
        context["UploaderCount"] = UploaderCount
        context["ApproverCount"] = ApproverCount    
        context["PublisherCount"] = PublisherCount
        context["totalUsers"] = totalUsers 

        
        Roles = ["No Role", "Admin", "Approver/Uploader", "Uploader/Publisher", "Approver/Publisher", "Uploaders", "Approver", "Publisher"]
        RoleCount = [NoRoleCount, AdminCount, ApproverUploaderCount, UploaderPublisherCount, ApproverPublisherCount, UploaderCount, ApproverCount,  PublisherCount]
        context["var"] = Roles
        context["val"] = RoleCount

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
        slug = ""
        if self.kwargs.get('slug'):            
            querySet = licenseData.objects.all()
            if self.kwargs['slug'] == "all":
                querySet = querySet
                slug = "Complete"
            elif self.kwargs['slug'] == "DraftorRejected":
                querySet = querySet.exclude(status = Status.objects.get(status = "Approved")) 
                slug = "Draft and Rejected"
            elif self.kwargs['slug'] in ["Approved", "Rejected", "Draft"]:
                querySet = querySet.filter(status = Status.objects.get(status = self.kwargs['slug']))
                slug = self.kwargs['slug']
            else:
                slug = "No such"
                querySet = None
        else:
            slug = "No such"
            querySet = None
        context['licenses'] = querySet  
        context['context'] = '{} License List'.format(slug)     
        return context 
    
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
            isExport = self.request.POST.get("action") == "Export"
            isExportAndZip = self.request.POST.get("action") == "ExportAndZip"
            request.session["list"] = licenseList
            if isExport and not isExportAndZip:
                return export(request)
            else:
                return exportAndZip(request)
        else:
            return exportAndZipApprover(request)


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
        context["ChangesTracking"] = False  
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
        context["ChangesTracking"] = True  
        return context  

@login_required
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

#approver Specific view
class SingleLicenseView(LoginRequiredMixin, View):
    def get(self, request, slug):
        licenseObject = licenseData.objects.get(id=slug)
        text = licenseObject.licenseData.split("\n")
        latestComments = licenseTracking.objects.filter(license = licenseObject).order_by("-date")[0]
        context = {
           "licenseObject" : licenseObject,
           "context" : "Detail of the License",
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
        if condition in ["Approver", "Uploader", "Publisher", "Admin"]:
            if condition == "Approver":
                context['Users'] = User.objects.filter(groups__name__in = [condition]).exclude(groups__name__in = ["Uploader", "Publisher"])
            elif condition == "Uploader":
                context['Users'] = User.objects.filter(groups__name__in = [condition]).exclude(groups__name__in = ["Approver", "Publisher"])
            elif condition == "Publisher":
                context['Users'] = User.objects.filter(groups__name__in = [condition]).exclude(groups__name__in = ["Approver", "Uploader"])
            else:
                context['Users'] = User.objects.filter(groups__name__in = [condition])
            context['context'] = '{} List'.format(condition)
        elif condition == "ApproverAndUploader":
            context['Users'] = User.objects.filter(groups__name__in = ["Approver"]).filter(groups__name__in = ["Uploader"])
            context['context'] = 'List of Users with roles Of'
            context['secondaryContext'] = ' both Approver and Uploader'
        elif condition == "ApproverAndPublisher":
            context['Users'] = User.objects.filter(groups__name__in = ["Approver"]).filter(groups__name__in = ["Publisher"])
            context['context'] = 'List of Users with roles Of'
            context['secondaryContext'] = ' both Approver and Publishers'
        elif condition == "UploaderAndPublisher":
            context['Users'] = User.objects.filter(groups__name__in = ["Uploader"]).filter(groups__name__in = ["Publisher"])
            context['context'] = 'List of Users with roles Of'
            context['secondaryContext'] = ' both Publisher and Uploader'
        elif condition == "ApproverAndUploaderAndPublisher":
            context['Users'] = User.objects.filter(groups__name__in = ["Approver"]).filter(groups__name__in = ["Uploader"]).filter(groups__name__in = ["Publisher"])
            context['context'] = 'List of Users with roles Of'
            context['secondaryContext'] = ' Approver, Uploader and Publisher'
        elif condition == 'NewUsers':
            context['Users'] = User.objects.exclude(groups__name__in = ["Approver","Uploader","Admin","Publisher"]).exclude(is_superuser=True)
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
        "isPublisher": False,
        "wrongSelection": False,
        "noSelection": False
    }
    if userObject.groups.exists():
        if "Approver" in list(userObject.groups.values_list('name', flat = True)): 
            context["isApprover"] = True
        if "Uploader" in list(userObject.groups.values_list('name', flat = True)): 
            context["isUploader"] = True
        if "Publisher" in list(userObject.groups.values_list('name', flat = True)): 
            context["isPublisher"] = True
        if "Admin" in list(userObject.groups.values_list('name', flat = True)): 
            context["isAdmin"] = True

    if request.method=="POST":
        if request.POST.get("Admin") != None:
            if request.POST.get("Uploader") == None and (request.POST.get("Approver") == None and request.POST.get("Publisher")):
                userObject.groups.clear()
                groupObject = Group.objects.get(name = "Admin")
                userObject.groups.add(groupObject)
                messages.success(request, "Role added successfully!")
                return redirect("user:users")
            else:
                context["wrongSelection"] = True
        elif request.POST.get("Uploader") != None or (request.POST.get("Approver") != None or request.POST.get("Publisher") != None):            
            userObject.groups.clear()
            if request.POST.get("Approver") != None:
                groupObject = Group.objects.get(name = "Approver")
                userObject.groups.add(groupObject)
            if request.POST.get("Uploader") != None:
                groupObject = Group.objects.get(name = "Uploader")
                userObject.groups.add(groupObject)
            if request.POST.get("Publisher") != None:
                groupObject = Group.objects.get(name = "Publisher")
                userObject.groups.add(groupObject)
            messages.success(request, "Role added successfully!")
            return redirect("user:dashboard")
        else:
            context["noSelection"] = True
    return render(request, "user/setGroups.html",context)

#User with no roles Specific Views
@login_required
def logoutAndLicenseList(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect("user_sign_in:displayApprovedLicenses")
    