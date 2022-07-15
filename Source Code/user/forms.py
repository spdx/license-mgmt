from django import forms
from .models import licenseData, namespace

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