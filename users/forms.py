from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Account
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text='email address required')

    class Meta:
        model = Account
        fields = ("email","username","phone","password1","password2",'first_name','last_name','wilaya','city','address','store_coordinates','documents1','documents2')


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ('username','password')
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not authenticate(username=username,password=password):
            raise forms.ValidationError("invalid login")