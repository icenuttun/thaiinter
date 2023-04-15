from django import forms
from .models import RoofTracking, ProcessName

class RoofTrackingForm(forms.ModelForm):
    process_name = forms.ModelChoiceField(queryset=ProcessName.objects.all(), empty_label='Select a process')
    note = forms.CharField(max_length=255, required=False)
    last_process = forms.BooleanField(required=False)
    
    class Meta:
        model = RoofTracking
        fields = ('process_name', 'note', 'last_process')
    
    def __init__(self, *args, **kwargs):
        super(RoofTrackingForm, self).__init__(*args, **kwargs)
        self.fields['process_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['note'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_process'].widget.attrs.update({'class': 'form-check-input'})


class ProcessNameForm(forms.ModelForm):
    class Meta:
        model = ProcessName
        fields = ['name']