from django import forms
from ..models.custom_user import CustomUser

class ResetPasswordForm(forms.Form):
	'''Classe permettant de creer un formulaire de reinitialisation du mot de passe'''
	class Meta:
		model = CustomUser
		fields = ['password1', 'password2'] 
	password1 = forms.CharField(
		label=('Mot de passe:'),
		widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
		help_text=('Votre mot de passe doit contenir au moins 8 caracteres')
	)
	password2 = forms.CharField(
		label=('Confirmer le mot de passe:'),
		widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
		help_text=('Re-entrez votre mot de passe pour confirmer')
	)