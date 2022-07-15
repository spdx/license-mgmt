from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import User

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