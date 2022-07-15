from django.db import models
from django.conf import settings
from datetime import datetime  
from django.core.validators import RegexValidator

# Create your models here.
class Status(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=25, null=False, blank=False)
    
    class Meta:
        db_table = "Status"

    def __str__(self):
        return self.status.lower()

class operationType(models.Model):
    id = models.AutoField(primary_key=True)
    operation = models.CharField(max_length=25, null=False, blank=False)

    class Meta:
        db_table = "Operation Types"

    def __str__(self):
        return self.operation

class namespace(models.Model):
    id = models.AutoField(primary_key=True)
    namespaceText = models.CharField(max_length=30, null=False, blank=False)

    class Meta:
        db_table = "Namespace"

    def __str__(self):
        return self.namespaceText
        
class licenseData(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    identifier = models.TextField(null=True, blank=True, unique=True, validators=[
            RegexValidator(
                regex="^[A-Za-z0-9.-]*$",
                message="Identifier should be a sequence of alphabets / digits / '-' / '.' ",
            ),
        ])
    namespace = models.ForeignKey(namespace, null=False, blank = False, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, null=False, blank = False, on_delete=models.PROTECT)
    licenseData = models.TextField(null=False, blank=False)

    class Meta:
        db_table = "License Data"

    def __str__(self):
        displayInfo = "{}-{}".format(self.namespace,self.title)
        return displayInfo

class licenseTracking(models.Model):
    id = models.AutoField(primary_key=True)
    license = models.ForeignKey(licenseData, null=False, blank=False, on_delete=models.CASCADE)
    operationType = models.ForeignKey(operationType, null=False, blank=False, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date = models.DateTimeField(default=datetime.now(), blank=False, null=False)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "License Tracking"
    
    def __str__(self):
        displayInfo = "{}: {}-{}".format(self.license,self.user,self.operationType)
        return displayInfo


