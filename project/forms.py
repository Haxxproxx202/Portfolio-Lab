from django import forms
from django.contrib.auth.models import User
from django.core.validators import ValidationError, EmailValidator
import re
from django.utils.translation import gettext as _


def pw_validator(value):
    if not re.findall(r'\d', value) or not re.findall('[A-Z]', value):
        raise forms.ValidationError(_('The password must contain at least 1 uppercase letter and 1 digit.'),
                                    code="Invalid - no uppercase letter or a digit in the password",
                                    params={'value': '1'})


def email_validator(value):
    if not EmailValidator(value):
        raise ValidationError(_("The email must be in format: my_email@example.com"))


class LoginForm(forms.Form):
    username = forms.EmailField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RemindPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=15,
                                 min_length=3,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=15,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=30,
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    pass1 = forms.CharField(max_length=20,
                            widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                            validators=[pw_validator])
    pass2 = forms.CharField(max_length=20,
                            widget=forms.PasswordInput(attrs={'placeholder': "Repeat Password"}))

    def clean(self):
        if self.data['pass1'] != self.data['pass2']:
            raise ValidationError(_("The passwords you entered do not match."),
                                  code="Invalid - passwords differ",
                                  params={'value': '2'})
        else:
            return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("User with that email already exists."),
                                        code="Invalid - email already in the database",
                                        params={'value': '3'})
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
            raise ValidationError(_('You entered two different passwords. Try again, please'),
                                  code="Invalid - passwords differ")
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
