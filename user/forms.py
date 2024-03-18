from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from user.models import Joining



class RegistrationForm(UserCreationForm):
    email=forms.EmailField( required=True)
    class Meta:
        model=User
        fields=['username', 'email', 'password1','password2']

        def __init__(self, *args, **kwargs):
            super(RegistrationForm, self). __init__( *args, **kwargs)
        
            for key, value in self.fields.items():
                value.widget.attrs.update({'class':'form-control'})
                # self.fields['email'].help_text =' <ul> <li>example@email.com </li> </ul> '


class SelfPersonForm(forms.ModelForm):

    class Meta:
        model= Joining
        fields= '__all__'
     