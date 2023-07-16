from django import forms
from .models import UserTimeCommitments 
from .widget import TimePickerInput
 
class CommitmentsForm(forms.ModelForm):
    hours_of_sleep = forms.IntegerField(label='', widget=forms.TextInput(attrs={'placeholder': 'Hours of Sleep'}))
    work_time_from = forms.TimeField(widget=TimePickerInput)
    work_time_to = forms.TimeField(widget=TimePickerInput)
    commute_time = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Hours to Commute'}))
    wake_time = forms.TimeField(widget=TimePickerInput)

    class Meta:
        model = UserTimeCommitments
        fields = ['hours_of_sleep', 'work_time_from', 'work_time_to', 'commute_time', 'wake_time']

        widgets = {
            
            'work_time_from' : TimePickerInput(),
        }

    # def __init__(self, *args, **kwargs):
    #     super(CommitmentsForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.label = ""