from django import forms
from django.contrib.auth.models import User
from django.core.validators import ValidationError

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=20, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    pass1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),)
    pass2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={'placeholder': "Repeat Password"}))

    def clean(self):
        print(self.data['pass1'], self.data['pass2'])
        if self.data['pass1'] != self.data['pass2']:
            raise ValidationError("The passwords you typed in do not match. Try again, please.")
        else:
            return super().clean()

class ChangePwForm(forms.Form):
    old_pw = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Old password'}))
    new_pw_1 = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    new_pw_2 = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    def clean(self):
        if self.data['new_pw_1'] != self.data['new_pw_2']:
            raise ValidationError('You typed two different passwords. Try again, please')
        else:

            return super().clean()


class ResetPwForm(forms.Form):
    new_pw_1 = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    new_pw_2 = forms.CharField(min_length=6, max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    def clean(self):
        if self.data['new_pw_1'] != self.data['new_pw_2']:
            raise ValidationError('You typed two different passwords. Try again, please')
        else:

            return super().clean()



