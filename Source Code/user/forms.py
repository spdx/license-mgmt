from django import forms
from .models import licenseData, exportHeaderFields

class licenseForm(forms.ModelForm):
    class Meta:
        model = licenseData
        exclude = ["id","status", "namespace"]
        labels = {
            "title": "License Title",
            "name": "License Name",
            "identifier": "License Identifier (optional)",
            "licenseData": "License Text"
        }

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title',
                                                                'class': 'form-control'
                                                                }))    
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name',
                                                                'class': 'form-control mb-4',
                                                                }))   
    identifier = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Identifier',
                                                                'class': 'form-control'
                                                                }))    
    licenseData = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'License Text',
                                                                'class': 'form-control',
                                                                "rows":5, 
                                                                "cols":20
                                                                }), required=False)

class ExportHeaderForm(forms.ModelForm):
    class Meta:
        model = exportHeaderFields
        exclude = ["id","creationInfoCreated", "user"]
    

    spdxVersion = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'spdxVersion',
                                                                'class': 'form-control'
                                                                }))    
    dataLicense = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'dataLicense',
                                                                'class': 'form-control',
                                                                }))   
    spdxId = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'spdxId',
                                                                'class': 'form-control'
                                                                }))    
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'name',
                                                                'class': 'form-control',
                                                                "rows":5, 
                                                                "cols":20
                                                                }), required=False)
    documentNamespace = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'documentNamespace',
                                                                'class': 'form-control',
                                                                "rows":5, 
                                                                "cols":20
                                                                }), required=False)
    
    creationInfoComment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'creationInfoComment',
                                                                'class': 'form-control'
                                                                }))    
    creationInfoCreatorsTools = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tools',
                                                                'class': 'form-control',
                                                                "rows":5, 
                                                                "cols":20
                                                                }), required=False)
    creationInfoCreatorsOrganization = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Organization',
                                                                'class': 'form-control',
                                                                "rows":5, 
                                                                "cols":20
                                                                }), required=False)
    creationInfoCreatorsPerson = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Person',
                                                                'class': 'form-control',
                                                                "rows":5, 
                                                                "cols":20
                                                                }), required=False)
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'comment',
                                                                'class': 'form-control',
                                                                "rows":5, 
                                                                "cols":20
                                                                }), required=False)