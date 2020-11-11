from django import forms
from authentication.models import *
from django.contrib.auth.forms import UserCreationForm


class UserSignUpForm(forms.Form):
    email = forms.CharField(required=True)
    username = forms.CharField(required=True)
    profession = forms.CharField(required=True)
    password = forms.CharField(required=True, )
    password2 = forms.CharField(required=False, )
