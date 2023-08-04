from django import forms
from .models import UserTimeCommitments 
from .widget import TimePickerInput

# Create the fields for the common commitments form
class CommitmentsForm(forms.ModelForm):
    hours_of_sleep = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Hours of Sleep'}))
    work_time_from = forms.TimeField(widget=TimePickerInput,required=False)
    work_time_to = forms.TimeField(widget=TimePickerInput,required=False)
    commute_time = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Hours to Commute'}),required=False)
    wake_time = forms.TimeField(widget=TimePickerInput,required=False)
    get_ready_time = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Hours to Get Ready for work'}),required=False)

    
    class Meta:
        # Map this form to the UserTimeCommitments model
        model = UserTimeCommitments
        # exclude the user from this mapping
        exclude = ('user',)
        # fields to include
        fields = ['hours_of_sleep', 'work_time_from', 'work_time_to', 'commute_time', 'wake_time', 'get_ready_time']

        # Add to picker widget to fields in the form
        widgets = {
            'work_time_from' : TimePickerInput(),
            'work_time_to' : TimePickerInput(),
            'wake_time' : TimePickerInput(),
        }
