from django import forms
from .models import User
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
