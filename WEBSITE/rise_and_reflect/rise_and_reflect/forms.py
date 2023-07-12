from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class MyCustomSignupForm(UserCreationForm):
    name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'phone', 'password1', 'password2', )