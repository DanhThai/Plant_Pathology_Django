from django.contrib.auth.forms import UserCreationForm
from django import forms

from UserProfile.models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'phone_number', 'age', 'address', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'phone_number', 'age', 'address')

class AvatarFrom(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('avatar',)
