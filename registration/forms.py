from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm:
	phone_number = forms.CharField(max_length = 255)
	

	class Meta:

		model = Account
		fields = ['username','email','phone_number','password1']