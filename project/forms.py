from django import forms
from django.contrib.auth.models import User
from django.core.validators import ValidationError, EmailValidator
from .validators import UppercaseValidator, NumberValidator
import re
from django.utils.translation import gettext as _


def pw_validator(value):
    if not re.findall('\d', value):
        raise ValidationError('Fail')
    if not re.findall('[A-Z]', value):
        raise ValidationError('Fail')


def email_validator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError("User with that email already exists")


class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RemindPasswordForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=20,
                                 min_length=3,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=30,
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    pass1 = forms.CharField(max_length=30,
                            widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                            validators=[pw_validator])
    pass2 = forms.CharField(max_length=30,
                            widget=forms.PasswordInput(attrs={'placeholder': "Repeat Password"}))

    def clean(self):
        if self.data['pass1'] != self.data['pass2']:
            print("Blad_3d")
            raise forms.ValidationError({'pass1': "The passwords you entered do not match. Try again, please."})
        else:
            return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(message="User with that email already exists.", code="email")
        return email


class ChangePwForm(forms.Form):
    current_pw = forms.CharField(max_length=20,
                                 widget=forms.PasswordInput(attrs={'placeholder': 'Old password',
                                                                   'style': 'border-radius: 5px'}))
    new_pw_1 = forms.CharField(min_length=6,
                               max_length=20,
                               widget=forms.PasswordInput(attrs={'placeholder': 'New password',
                                                                 'style': 'border-radius: 5px'}),
                               validators=[pw_validator])
    new_pw_2 = forms.CharField(min_length=6,
                               max_length=20,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password',
                                                                 'style': 'border-radius: 5px'}))

    def clean(self):
        if self.data['new_pw_1'] != self.data['new_pw_2']:
            raise ValidationError('You entered two different passwords. Try again, please')
        else:

            return super().clean()


class ResetPwForm(forms.Form):
    new_pw_1 = forms.CharField(min_length=6,
                               max_length=20,
                               widget=forms.PasswordInput(attrs={'placeholder': 'New password'}),
                               validators=[pw_validator])
    new_pw_2 = forms.CharField(min_length=6,
                               max_length=20,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    def clean(self):
        if self.data['new_pw_1'] != self.data['new_pw_2']:
            raise forms.ValidationError({'new_pw_1': "Fail"})
        else:
            return super().clean()



