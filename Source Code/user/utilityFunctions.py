from contextlib import nullcontext
from pprint import isreadable
from .models import Status, licenseData, licenseTracking, operationType, namespace
from datetime import datetime as dt
from .forms import licenseForm, ExportHeaderForm
from wsgiref.util import FileWrapper
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import datetime
import zipfile, os, requests, json, tempfile
import re
from io import BytesIO
#model import
from user.models import licenseData, exportHeaderFields, Status, licenseTracking, operationType
from user.resources import licenseDataResource

def saveLicense(form, status, text):
    filledForm = form.save(commit=False)   
    filledForm.status = Status.objects.get(status = status.capitalize())
    filledForm.licenseData = text
    filledForm.namespace = namespace.objects.all()[0]
    filledForm.save()

def validityAndText(form, fileUpload):
    isBothSelected = True
    if form.cleaned_data['licenseData'].strip() == "":
        isBothSelected = False
    if fileUpload == None:
        if not isBothSelected:
            return True
        else:
            return [False, form.cleaned_data['licenseData'].strip()]
    else:
        if isBothSelected:
            return True
        else:
            return [False, fileUpload]


def duplicateCheck(text, name):    
    isDuplicate = True
    try:
        licenseData.objects.get(licenseData = text)     
    except:
        isDuplicate = False    
    return isDuplicate   

def licenseTrackingFunction(name, user, operation, comments):
    licenseObject = licenseData.objects.get(name = name)
    if operation == "new":
        operationTypeObject = operationType.objects.get(operation = 'New')
    elif operation == "modified":
        operationTypeObject = operationType.objects.get(operation = 'Modified')
    elif operation == "approved":
        operationTypeObject = operationType.objects.get(operation = 'Approved')
    else:
        operationTypeObject = operationType.objects.get(operation = 'Rejected')
    newLicenseTracking = licenseTracking.objects.create(
        license = licenseObject,
        operationType =  operationTypeObject,
        user = user,
        date =dt.now(),
        comments = comments )
    newLicenseTracking.save()

def dashboardOverallStats():
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
    return (pendingLicenses, approvedLicenses, rejectedLicenses, uploadedLicenses)

def UserCount(User):
    try:
        ApproverCount = User.objects.filter(groups__name__in = ["Approver"]).exclude(groups__name__in = ["Uploader"]).exclude(groups__name__in = ["Publisher"]).count()
    except:
        ApproverCount = 0    
    try:
        UploaderCount  =  User.objects.filter(groups__name__in = ["Uploader"]).exclude(groups__name__in = ["Approver"]).exclude(groups__name__in = ["Publisher"]).count()
    except:
        UploaderCount = 0    
    try:
        PublisherCount  =  User.objects.filter(groups__name__in = ["Publisher"]).exclude(groups__name__in = ["Approver"]).exclude(groups__name__in = ["Uploader"]).count()
    except:
        PublisherCount = 0 
    try:
        ApproverPublisherCount = User.objects.filter(groups__name__in = ["Approver"]).filter(groups__name__in = ["Publisher"]).exclude(groups__name__in = ["Uploader"]).count()
    except:
        ApproverPublisherCount = 0    
    try:
        ApproverUploaderCount = User.objects.filter(groups__name__in = ["Approver"]).filter(groups__name__in = ["Uploader"]).exclude(groups__name__in = ["Publisher"]).count()
    except:
        ApproverUploaderCount = 0   
    try:
        ApproverUploaderCount = User.objects.filter(groups__name__in = ["Approver"]).filter(groups__name__in = ["Uploader"]).exclude(groups__name__in = ["Publisher"]).count()
    except:
        ApproverUploaderCount = 0   
    try:
        UploaderPublisherCount = User.objects.filter(groups__name__in = ["Uploader"]).filter(groups__name__in = ["Publisher"]).exclude(groups__name__in = ["Approver"]).count()
    except:
        UploaderPublisherCount = 0   
    try:
        AdminCount = User.objects.filter(groups__name__in = ["Admin"]).count()
    except:
        AdminCount = 0     
    try:
        NoRoleCount = User.objects.exclude(groups__name__in = ["Approver","Uploader","Admin","Publisher"]).exclude(is_superuser=True).count()
    except:
        NoRoleCount = 0    
    try:
        totalUsers = User.objects.exclude(is_superuser=True).count()
    except:
        totalUsers = 0
    return (NoRoleCount, AdminCount, ApproverUploaderCount, UploaderPublisherCount, ApproverPublisherCount, UploaderCount, ApproverCount, PublisherCount, totalUsers)


def getChartsDetails(request):
    user = request.user
    role = request.session["role"]

    LicenseStatus = []
    LicenseStatusCount = []    
    if "Uploader" in role:
        NewLicensesCount = licenseTracking.objects.filter(operationType = operationType.objects.get(operation = "New"))
        NewLicensesCount = NewLicensesCount.filter(user = user)
        ModifiedLicensesCount = licenseTracking.objects.filter(operationType = operationType.objects.get(operation = "Modified"))
        ModifiedLicensesCount = ModifiedLicensesCount.filter(user = user)
        allLicensesCount = NewLicensesCount.count() + ModifiedLicensesCount.count()  
        LicenseStatus.append("All")
        LicenseStatus.append("New Licenses")
        LicenseStatus.append("Modified Licenses")
        LicenseStatusCount.append(allLicensesCount)
        LicenseStatusCount.append(NewLicensesCount.count())
        LicenseStatusCount.append(ModifiedLicensesCount.count())
    if "Approver" in role:
        approvedLicensesCount = licenseTracking.objects.filter(operationType = operationType.objects.get(operation = "Approved"))
        approvedLicensesCount = approvedLicensesCount.filter(user = user)
        rejectedLicensesCount = licenseTracking.objects.filter(operationType = operationType.objects.get(operation = "Rejected"))
        rejectedLicensesCount = rejectedLicensesCount.filter(user = user)
        allLicensesCount = approvedLicensesCount.count() + rejectedLicensesCount.count()  
        if "All" in LicenseStatus:
            LicenseStatusCount[0] += allLicensesCount
        else:
            LicenseStatus.append("All")
            LicenseStatusCount.append(allLicensesCount)
        LicenseStatus.append("Approved Licenses")
        LicenseStatus.append("Rejected Licenses")
        LicenseStatusCount.append(approvedLicensesCount.count())
        LicenseStatusCount.append(rejectedLicensesCount.count())
    if len(LicenseStatusCount)==0 and "Publisher" in role:
        approvedLicensesCount = licenseData.objects.filter(status = Status.objects.get(status = "Approved"))
        allLicensesCount = licenseData.objects.all()
        LicenseStatus = ["All", "Accepted"]
        LicenseStatusCount = [allLicensesCount.count(), approvedLicensesCount.count()]
    return(LicenseStatus, LicenseStatusCount)


def saveHeaderInfo(form, user):
    filledForm = form.save(commit=False)
    try: 
        ExportHeaderForm.objects.get(user = user)
    except:
        filledForm.user = user
    filledForm.creationInfoCreated = dt.now()
    filledForm.save()

def buildExportFile(list, newHeaderInfo):
    hasExtractedLicensingInfos = []
    for licenseId in list:
        license = licenseData.objects.get(id = licenseId)
        text = license.licenseData
        identifier = license.identifier
        seeAlsos = re.findall(r"((?:(?<=[^a-zA-Z0-9]){0,}(?:(?:https?\:\/\/){0,1}(?:[a-zA-Z0-9\%]{1,}\:[a-zA-Z0-9\%]{1,}[@]){,1})(?:(?:\w{1,}\.{1}){1,5}(?:(?:[a-zA-Z]){1,})|(?:[a-zA-Z]{1,}\/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\:[0-9]{1,4}){1})){1}(?:(?:(?:\/{0,1}(?:[a-zA-Z0-9\-\_\=\-]){1,})*)(?:[?][a-zA-Z0-9\=\%\&\_\-]{1,}){0,1})(?:\.(?:[a-zA-Z0-9]){0,}){0,1})", text)
        comment = licenseTracking.objects.filter(license = license).order_by("-date")[0].comments        
        if len(seeAlsos) != 0:
            hasExtractedLicensingInfos.append({"licenseId": identifier, "extractedText": text, "comment": comment, "seeAlsos": seeAlsos})
        else:
            hasExtractedLicensingInfos.append({"licenseId": identifier, "extractedText": text, "comment": comment})    
    licenseDict = {}
    licenseDict["spdxVersion"] = newHeaderInfo.spdxVersion 
    licenseDict["dataLicense"] = newHeaderInfo.dataLicense
    licenseDict["spdxId"] = newHeaderInfo.spdxId 
    licenseDict["name"] = newHeaderInfo.name
    licenseDict["documentNamespace"] = newHeaderInfo.documentNamespace
    licenseDict["creationInfo"] = dict()
    licenseDict["creationInfo"]["comment"] = newHeaderInfo.creationInfoComment
    licenseDict["creationInfo"]["created"] = str(newHeaderInfo.creationInfoCreated)
    creatorInfo = []
    creatorInfo.append("Tool:{}".format(newHeaderInfo.creationInfoCreatorsTools))
    creatorInfo.append("Organization:{}".format(newHeaderInfo.creationInfoCreatorsOrganization))
    creatorInfo.append("Person:{}".format(newHeaderInfo.creationInfoCreatorsPerson))
    licenseDict["creationInfo"]["creators"] = creatorInfo    
    licenseDict["comment"] = newHeaderInfo.comment
    licenseDict["hasExtractedLicensingInfos"] = hasExtractedLicensingInfos
    jsonLicenseExport = json.dumps(licenseDict, indent = 4) 
    return jsonLicenseExport


def export(request, newHeaderInfo = None):
    if newHeaderInfo == None:       
        request.session["Option"] = "export"
        return redirect("user:headerReview")

    list = request.session["list"]
    if(list == None):
        messages.warning(request, "Do not refresh the Header screen")
        return redirect("user:viewLicenses", slug="Approved")
    jsonLicenseExport = buildExportFile(list, newHeaderInfo)  
    response = HttpResponse(jsonLicenseExport, content_type = "application/json")
    response['Content-Disposition'] = 'attachment; filename=License List' + str(datetime.datetime.now()) + \
        '.json'
    request.session["list"] = None
    return response

def exportAndZip(request, newHeaderInfo = None):
    if newHeaderInfo == None:       
        request.session["Option"] = "zip"
        return redirect("user:headerReview")

    #newHeaderInfo = headerData #This has to be deleted
    list = request.session["list"]
    if(list == None):
        messages.warning(request, "Do not refresh the Header screen")
        return redirect("user:viewLicenses", slug="Approved")
    jsonLicenseExport = buildExportFile(list, newHeaderInfo)  
    in_memory = BytesIO()
    zf = zipfile.ZipFile(in_memory, mode="w")    
    #If you have data in text format that you want to save into the zip as a file
    zf.writestr('License List' + str(datetime.datetime.now()) + '.json', jsonLicenseExport)    
    #Close the zip file
    zf.close()
    #Go to beginning
    in_memory.seek(0)    
    #read the data
    data = in_memory.read()
    response = HttpResponse(data, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=Zip List' + str(datetime.datetime.now()) + '.zip'
    request.session["list"] = None
    return response  



def ApproverJSONBuilder(id):
    licenseObject = licenseData.objects.get(id = id)
    licenseJson = {}
    licenseJson["title"] = licenseObject.title
    licenseJson["name"] = licenseObject.name 
    licenseJson["identifier"] = licenseObject.identifier 
    licenseJson["namespace"] = str(licenseObject.namespace)
    licenseJson["licenseData"] = licenseObject.licenseData 
    jsonLicenseExport = json.dumps(licenseJson, indent = 4) 
    return jsonLicenseExport

def exportAndZipApprover(request):
    in_memory = BytesIO()
    zf = zipfile.ZipFile(in_memory, mode="w")    
    #If you have data in text format that you want to save into the zip as a file    
    licenseObjects = licenseData.objects.filter(status = Status.objects.get(status = "Draft"))
    for license in licenseObjects:
        zf.writestr('{}: {}'.format(license.id,license.title) + '.json', ApproverJSONBuilder(license.id))    
    #Close the zip file
    zf.close()
    #Go to beginning
    in_memory.seek(0)    
    #read the data
    data = in_memory.read()
    response = HttpResponse(data, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=Zip List' + str(datetime.datetime.now()) + '.zip'
    request.session["list"] = None
    return response 