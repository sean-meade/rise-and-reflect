from django import forms

# widget used to add the timeinput field on the form for time commitments
class TimePickerInput(forms.TimeInput):
    input_type = 'time'