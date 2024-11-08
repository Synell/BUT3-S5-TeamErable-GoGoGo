from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models.custom_user import CustomUser

class SignUpForm(UserCreationForm):
	'''Classe permettant de creer un formulaire de creation d'utilisateur'''
	class Meta:
		model = CustomUser
		fields = ['username', 'email', 'password1', 'password2'] 

	username = forms.CharField()
	password1 = forms.CharField()
	password2 = forms.CharField()
	email = forms.EmailField()
