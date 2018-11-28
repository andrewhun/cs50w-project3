from django import forms
from django.forms import widgets, ModelForm, Select

class RegisterForm(forms.Form):
	
	reg_firstname = forms.CharField(label = "First name:")
	reg_lastname = forms.CharField(label = "Last name:")
	reg_email = forms.EmailField(label = "Email address")
	reg_user = forms.CharField(label = "Username:")
	reg_pw = forms.CharField(widget = widgets.PasswordInput(), label = "Password")
	reg_conf = forms.CharField(widget = widgets.PasswordInput(), label = "Confirm password",
	 empty_value = "Confirm password")

class LoginForm(forms.Form):
	
	login_user = forms.CharField(label = "Username", empty_value = "Username")
	login_pw = forms.CharField(widget = widgets.PasswordInput(), label = "Password", empty_value = "Password")
