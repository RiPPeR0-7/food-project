from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from . models import Contact, Profile, Shopcart

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'message']

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length = 150)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

STATE= [
    ('Abuja','Abuja'),
    ('Abia','Abia'),
    ('Edo','Edo'),
    ('Delta','Delta'),
    ('Kogi','kogi')
]

class ProfileUpdate(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['first_name','last_name','phone','address','state','pix']
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Adress'}),
            'state':forms.Select(attrs={'class':'form-control','placeholder':'State'}, choices=STATE),
            'pix':forms.FileInput(attrs={'class':'form-control'})
        }

class ShopcartForm(forms.ModelForm):
    
    class Meta:
        model = Shopcart
        fields = ['quantity']
