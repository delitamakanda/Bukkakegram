from django import forms
from django.forms import ModelForm
from .models import Bukkake, User
from django.contrib.auth.forms import UserCreationForm
from cloudinary.forms import CloudinaryJsFileField, CloudinaryUnsignedJsFileField
from cloudinary.compat import to_bytes
import cloudinary, hashlib

#Create forms
class BukkakeForm(ModelForm):
    name = forms.CharField(label='Name', max_length=250, widget=forms.TextInput(attrs={'class': 'form-control'}))
    value = forms.DecimalField(label='Value', max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    material = forms.CharField(label='Material', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(label='Location', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #image = CloudinaryJsFileField()

    class Meta:
        model = Bukkake
        #fields = '__all__'
        exclude = ('likes','user',)
        #fields = ['name', 'value', 'material', 'location', 'image',]
    #name = forms.CharField(label='Name', max_length=100)
    #value = forms.DecimalField(label='Value', max_digits=10, decimal_places=2)
    #material = forms.CharField(label='Material', max_length=100)
    #location = forms.CharField(label='Location', max_length=100)
    #img_url = forms.CharField(label='Image Url', max_length=255)

class PhotoDirectForm(BukkakeForm):
    image = CloudinaryJsFileField()

class PhotoUnsignedDirectForm(BukkakeForm):
    upload_preset_name = "sample_" + hashlib.sha1(to_bytes(cloudinary.config().api_key + cloudinary.config().api_secret)).hexdigest()[0:10]
    image = CloudinaryUnsignedJsFileField(upload_preset_name)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email Address', max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First name', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last name', max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    #def verify_password(self):
    #    if 'password1' in self.cleaned_data:
    #        password1 = self.cleaned_data['password1']
    #        password2 = self.cleaned_data['password2']
    #        if password == password2:
    #            return password2
    #    raise forms.ValidationError('Passwords do not match')

    #def unique_username(self):
    #    username = self.cleaned_data['username']
    #    if not re.search(r'^\w+$', username):
    #        raise forms.ValidationError('Username can only contain alphanumeric and the underscore')
    #    try:
    #        User.objects.get(username=username)
    #    except ObjectDoesNotExist:
    #        return username
    #    raise forms.ValidationError('Username already taken')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]
        exclude = ('first_name', 'last_name',)

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

# Create your views here.
#def index(request):
#    bukkakes = Bukkake.objects.all()
#    return render(request,'index.html', {'bukkakes':bukkakes})

#class Bukkake:
    #def __init__(self, name, value, material, location):
        #self.name = name
        #self.value = value
        #self.material = material
        #self.location = location

#bukkakes = [
    #Bukkake('Pute de Luxe', 120.00, 'Cashmere', "Budapest")
    #Bukkake('Le Bonheur', 0.00, 'Velvet', "Paris")
    #Bukkake('Musique rock', 0.99, 'Fire', "USA")
#]
