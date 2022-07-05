from .models import Status, licenseData, licenseTracking, operationType, namespace
from datetime import datetime
from .forms import licenseForm

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
    try:
        licenseData.objects.get(licenseData = text).exclude(name = name)
        isDuplicate = True
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
        date =datetime.now(),
        comments = comments )
    newLicenseTracking.save()