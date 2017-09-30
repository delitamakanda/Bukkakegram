from django import forms
from django.conf import settings
from django.forms import ModelForm
from .models import Bukkake, User
from django.contrib.auth.forms import UserCreationForm
from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
from cloudinary.compat import to_bytes
import cloudinary, hashlib

#Create forms
class BukkakeForm(ModelForm):
    name = forms.CharField(label='Name', max_length=250)
    value = forms.DecimalField(label='Value', max_digits=10, decimal_places=2)
    material = forms.CharField(label='Material', max_length=100)
    location = forms.CharField(label='Location', max_length=100)
    description = forms.CharField(label='Description')

    class Meta:
        model = Bukkake
        fields = "__all__"

class PhotoDirectForm(BukkakeForm):
    image = CloudinaryJsFileField()

class PhotoUnsignedDirectForm(BukkakeForm):
    upload_preset_name = "sample_" + hashlib.sha1(to_bytes(cloudinary.config().api_key + cloudinary.config().api_secret)).hexdigest()[0:10]
    image = CloudinaryUnsignedJsFileField(upload_preset_name)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=64)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email Address', max_length=255, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user
