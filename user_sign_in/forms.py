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
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from user_sign_in.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                                'class': 'form-control'
                                                                }))    
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                                'class': 'form-control mb-4',
                                                                }))   
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name',
                                                                'class': 'form-control'
                                                                }))    
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name',
                                                                'class': 'form-control'
                                                                }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                'class': 'form-control mb-4',
                                                                'id': 'password',
                                                                'name': 'passord'
                                                                }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                'class': 'form-control mb-4',
                                                                'id': 'password',
                                                                'name': 'passord'
                                                                }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = "Confirm Password"
        self.fields['password1'].label = "Password"
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
     


class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']
    
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                                'class': 'form-control'
                                                                }))    
     
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                'class': 'form-control mb-4',
                                                                'id': 'password',
                                                                'name': 'passord'
                                                                }))


    
class modifyUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
          'first_name',
          'last_name',
          'username',
          'email',
        )
        exclude = ('password',)
    
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                                'class': 'form-control'
                                                                }))    
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                                'class': 'form-control mb-4',
                                                                }))   
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name',
                                                                'class': 'form-control'
                                                                }))    
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name',
                                                                'class': 'form-control'
                                                                }))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"


class NewPasswordResetForm(PasswordResetForm):
    fields = ['email']
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': '',
                                                                'class': 'form-control mb-4',
                                                                })) 