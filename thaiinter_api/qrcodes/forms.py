from django import forms
from .models import MetalSheetRoof, RoofType, RoofColor, RoofSize

class MetalSheetRoofForm(forms.ModelForm):
    roof_type = forms.ModelChoiceField(queryset=RoofType.objects.all(), empty_label='Select a roof type')
    size = forms.ModelChoiceField(queryset=RoofSize.objects.all(), empty_label='Select a size')
    color = forms.ModelChoiceField(queryset=RoofColor.objects.all(), empty_label='Select a roof color')
    quantity = forms.IntegerField()
    
    class Meta:
        model = MetalSheetRoof
        fields = ('roof_type', 'size', 'color', 'quantity')
    
    def __init__(self, *args, **kwargs):
        super(MetalSheetRoofForm, self).__init__(*args, **kwargs)
        self.fields['roof_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['size'].widget.attrs.update({'class': 'form-control'})
        self.fields['color'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})

class RoofColorForm(forms.ModelForm):
    class Meta:
        model = RoofColor
        fields = ['name']

class RoofTypeForm(forms.ModelForm):
    class Meta:
        model = RoofType
        fields = ['name']

class RoofSizeForm(forms.ModelForm):
    class Meta:
        model = RoofSize
        fields = ['name']