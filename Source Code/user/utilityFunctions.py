from pprint import isreadable
from .models import Status, licenseData, licenseTracking, operationType, namespace
from datetime import datetime as dt
from .forms import licenseForm, ExportHeaderForm
from django.http import HttpResponse
from django.shortcuts import render
import datetime
import zipfile, os, io, requests
import re
#model import
from user.models import licenseData
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


def saveHeaderInfo(form, user):
    filledForm = form.save(commit=False)
    try: 
        ExportHeaderForm.objects.get(user = user)
    except:
        filledForm.user = user
    filledForm.creationInfoCreated = dt.now()
    filledForm.save()

def buildExportFile(list):
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
    
    return(hasExtractedLicensingInfos)

def export(list):
    # licenseResource = licenseDataResource()
    # dataset = licenseResource.export()
    # response = HttpResponse(dataset.json, content_type = "application/json")
    # response['Content-Disposition'] = 'attachment; filename=License List' + str(datetime.datetime.now()) + \
    #     '.json'
    # return response
    hasExtractedLicensingInfos = buildExportFile(list)
    

