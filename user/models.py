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
    SimplifiedlicenseData = models.TextField(default ="", null=False, blank=False)

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


class exportHeaderFields(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    spdxVersion = models.CharField(max_length=100, null=False, blank=False)
    dataLicense = models.CharField(max_length=100, null=False, blank=False)
    spdxId = models.CharField(max_length=100, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    documentNamespace = models.CharField(max_length=100, null=False, blank=False)
    creationInfoComment = models.TextField(null=False, blank=False)
    creationInfoCreated = models.DateTimeField(default=datetime.now(), blank=False, null=False)
    creationInfoCreatorsTools = models.CharField(max_length=100, blank=False, null=False)
    creationInfoCreatorsOrganization = models.CharField(max_length=100, blank=False, null=False)
    creationInfoCreatorsPerson = models.CharField(max_length=100,blank=False, null=False)
    comment = models.TextField(null=False, blank=False)