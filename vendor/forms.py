from django import forms
from .models import Vendor, OpenHour
from accounts.validators import allow_only_images_validator

class VendorForm(forms.ModelForm):
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']

class OpenHourForm(forms.ModelForm):
    class Meta:
        model = OpenHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']
