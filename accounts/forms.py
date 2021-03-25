from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class SignUpForm(UserCreationForm):
    '''This is the signup form with email and password required'''
    email = forms.EmailField(
        max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = CustomUser
        fields = [
            'email', 
            'password1', 
            'password2', 
            ]

class ProfileForm(forms.ModelForm):
    '''This displays and allows changes to the Users profile with his email'''

    class Meta:
        model = CustomUser
        fields = [
            'email',
            ]

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = CustomUser
        fields = ("email",)