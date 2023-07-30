from django import forms
from allauth.account.forms import SignupForm
from .models import UserProfile
 
# Class to customize the signup form to include the name and phone number
class CustomSignupForm(SignupForm):
    # Create the extra form fileds
    name = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    phone = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    # Override what happens when the user is saved on submitting the signup form
    def save(self, request):

        # Add the name and phone number and then save
        user = super(CustomSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']
        user.save()
        # Create your user profile with these extra fields
        user_profile = UserProfile(user=user, name=self.cleaned_data['name'], phone=self.cleaned_data['phone'])
        user_profile.save()

    # On initial creation of the form add form-control class and remove labels.
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.label = ""