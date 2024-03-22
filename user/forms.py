from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField,PasswordChangeForm,SetPasswordForm,PasswordResetForm

from django.contrib.auth.models import User

from user.models import Joining

class MyPasswordChangeForm(PasswordChangeForm):
    old_password= forms.CharField(label='old Password',widget= forms.PasswordInput(attrs={'autofocus': 'True','autocomplete':'current-password','class': 'form-control'}))
    new_password1= forms.CharField(label='New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))
    new_password2= forms.CharField(label='Confirm New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))



class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))



class MySetPasswordForm(SetPasswordForm):
    new_password1= forms.CharField(label='New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))
    new_password2= forms.CharField(label='Confirm New Password',widget= forms.PasswordInput(attrs={'autocomplete':'current-password','class': 'form-control'}))


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
     