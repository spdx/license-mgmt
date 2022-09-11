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


from django import forms
from .models import licenseData, exportHeaderFields

class licenseForm(forms.ModelForm):
    class Meta:
        model = licenseData
        exclude = ["id","status", "namespace", "SimplifiedlicenseData"]
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
        exclude = ["id","creationInfoCreated", "user", "spdxVersion", "dataLicense"]   

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