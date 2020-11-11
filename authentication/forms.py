
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from authentication.models import User

class loginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}),label="UserName")
    password = forms.CharField(widget=forms.PasswordInput(attrs= {'placeholder':'password'}),label="PassWord")


class registerForm(UserCreationForm):
	username = forms.CharField(help_text='Note:Your Username Must Not Contain Spaces', 
    widget= forms.TextInput(attrs={'placeholder':'Username'}))
	email = forms.EmailField(widget= forms.EmailInput(attrs={'placeholder':'Email'}),label= "Email")
	password1 = forms.CharField(widget= forms.PasswordInput(attrs={'placeholder':'Pssword'}),label="Password")
	password2 = forms.CharField(widget= forms.PasswordInput(attrs={'placeholder':'Confirm Password'}),label="Confirm Password")
	
	class Meta:
		model = User
		fields = ('username','email','password1','password2')

		# def save(self, commit=True):
		# 	user = super(registerForm, self).save(commit=False)
		# 	user = self.cleaned_data['email']
		# 	if commit:
		# 		user.save()
		# 	return user