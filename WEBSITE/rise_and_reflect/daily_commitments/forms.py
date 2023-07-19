from django import forms
from .models import UserTimeCommitments 
from .widget import TimePickerInput
 
class CommitmentsForm(forms.ModelForm):
    hours_of_sleep = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Hours of Sleep'}))
    work_time_from = forms.TimeField(widget=TimePickerInput,required=False)
    work_time_to = forms.TimeField(widget=TimePickerInput,required=False)
    commute_time = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Hours to Commute'}),required=False)
    wake_time = forms.TimeField(widget=TimePickerInput, required=False)
    get_ready_time = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Hours to Get Ready for work'}),required=False)

    class Meta:
        model = UserTimeCommitments
        exclude = ('user',)
        fields = ['hours_of_sleep', 'work_time_from', 'work_time_to', 'commute_time', 'wake_time', 'get_ready_time']

        widgets = {
            
            'work_time_from' : TimePickerInput(),
            'work_time_to' : TimePickerInput(),
            'wake_time' : TimePickerInput(),
        }
