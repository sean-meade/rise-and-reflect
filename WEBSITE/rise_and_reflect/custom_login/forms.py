from django import forms
from allauth.account.forms import SignupForm
from .models import UserProfile
 
 
class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    phone = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']
        user.save()
        # Create your user profile
        UserProfile.objects.create(user=user, name=self.cleaned_data['name'], phone=self.cleaned_data['phone'])

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.label = ""