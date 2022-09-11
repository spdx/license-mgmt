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


from django.contrib import admin
from .models import Status, exportHeaderFields, operationType, licenseData, licenseTracking, namespace
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class LisenceDataAdmin(ImportExportModelAdmin):
    list_display = ('title', 'namespace', 'name')
    list_filter = ('namespace', 'name')

class LisenceTrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'license','comments')
    list_filter = ('user', 'license')

admin.site.register(Status)
admin.site.register(namespace)
admin.site.register(operationType)
admin.site.register(licenseData, LisenceDataAdmin)
admin.site.register(licenseTracking, LisenceTrackingAdmin)
