from django import forms
from django.core.validators import ValidationError
from .validators import UppercaseValidator, NumberValidator
from django.contrib.auth.password_validation import validate_password
import re
from django.utils.translation import gettext as _


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=20,
                                 min_length=3,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=30,
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    pass1 = forms.CharField(max_length=30,
                            widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    pass2 = forms.CharField(max_length=30,
                            widget=forms.PasswordInput(attrs={'placeholder': "Repeat Password"}))

    def clean(self):
        if self.data['pass1'] != self.data['pass2']:
            raise ValidationError("The passwords you entered do not match. Try again, please.")
        else:
            return super().clean()


def pw_validator(value):
    if not re.findall('\d', value):
        raise ValidationError('no_digit')
    if not re.findall('[A-Z]', value):
        raise ValidationError('no_uppercase_letter')


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
                               widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    new_pw_2 = forms.CharField(min_length=6,
                               max_length=20,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    def clean(self):
        if self.data['new_pw_1'] != self.data['new_pw_2']:
            raise ValidationError('You entered two different passwords. Try again, please')
        else:
            return super().clean()



