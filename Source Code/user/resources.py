from import_export import resources
from .models import licenseData

class licenseDataResource(resources.ModelResource):
    class Meta:
        model = licenseData