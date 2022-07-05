from django.contrib import admin
from .models import Status, operationType, licenseData, licenseTracking, namespace
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

