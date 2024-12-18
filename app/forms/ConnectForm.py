from django import forms
from django.contrib.auth.forms import forms
from ..models.custom_user import CustomUser

class ConnectForm(forms.Form):
	'''Classe permettant de creer un formulaire de connexion'''
	class Meta:
		model = CustomUser
		fields = ['username', 'password']

	username = forms.CharField()
	password = forms.CharField()
