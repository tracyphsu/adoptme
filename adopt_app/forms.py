from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['user']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = '__all__'

class AdoptForm(forms.ModelForm):
    class Meta:
        model = Adopt
        fields = '__all__'