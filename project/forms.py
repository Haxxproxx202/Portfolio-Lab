from django import forms
from django.contrib.auth.models import User
from django.core.validators import ValidationError

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    pass1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),)
    pass2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': "Repeat Password"}))

    def clean(self):
        if self.data['pass1'] != self.data['pass2']:
            raise ValidationError("The passwords you typed in do not match. Try again, please.")
        else:
            return super().clean()
