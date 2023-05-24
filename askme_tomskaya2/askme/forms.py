from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from askme.models import *
import re

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(min_length=4, widget=forms.TextInput(attrs={"type": "password"}))
    continue_ = forms.CharField(widget=forms.HiddenInput(), initial='index')

    # def clean_password(self):
    #     data = self.cleaned_data['password']
    #     if data == 'wrong':
    #         raise ValidationError('Wrong password:')
    #     return data


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    continue_ = forms.CharField(widget=forms.HiddenInput(), initial='index')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_username(self):
        regex = r'^[a-zA-Z0-9_]+$'
        data = self.cleaned_data['username']

        if not re.fullmatch(regex, data):
            raise ValidationError('This username is prohibited')
        return data

    def clean_first_name(self):
        regex = r'^[a-zA-Z]+$'
        data = self.cleaned_data['first_name']
        if not re.fullmatch(regex, data):
            raise ValidationError('This first name is prohibited')

    def clean_last_name(self):
        regex = r'^[a-zA-Z]+$'
        data = self.cleaned_data['last_name']
        if not re.fullmatch(regex, data):
            raise ValidationError('This last name is prohibited')

    def clean_email(self):
        data = self.cleaned_data['email']
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, data):
            print("Valid email")
            raise ValidationError('Invalid email')
        return data


    def clean_password_check(self):
        data = self.cleaned_data['password_check']
        pas = self.cleaned_data['password']
        if not data == pas:
            raise ValidationError('Passwords must be equal')


class SettingsForm(forms.ModelForm):
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.initial['username'] = self.instance.username
            self.initial['email'] = self.instance.email




