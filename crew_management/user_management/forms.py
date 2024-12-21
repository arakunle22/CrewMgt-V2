from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-transparent',
            'placeholder': 'Email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-transparent',
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-transparent',
            'placeholder': 'Password',
            'autocomplete': 'new-password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-transparent',
            'placeholder': 'Repeat Password',
            'autocomplete': 'new-password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_approved = False
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-transparent',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-transparent',
            'placeholder': 'Password'
        })
    )

