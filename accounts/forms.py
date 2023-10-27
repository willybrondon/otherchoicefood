from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator
class UserForm(forms.ModelForm):
    class Meta:
        confirm_password = forms.CharField(widget=forms.PasswordInput())
        password = forms.CharField(widget=forms.PasswordInput())
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password'] # remove phone number phone_number on the list
    def clean(self):
        clean_data = super(UserForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password :
            raise forms.ValidationError('password does not match')
class UserProfileForm(forms.ModelForm):
    address = forms.FileField(widget=forms.TextInput(attrs={'placeholder':'start typing ...', 'required':'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])
    
    latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    
    class Meta :
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'city', 'pin_code', 'latitude', 'longitude']
    
def __init__(self, *args, **kwargs):
    super(UserProfileForm, self).__init__(*args, **kwargs)
    for field in self.fields:
        if field == 'latitude' or field == 'longitude':
            self.fields[field].widget.attrs['readonly'] = 'readonly'