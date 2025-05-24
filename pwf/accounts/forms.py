from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username',
        'autocomplete': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password',
        'autocomplete': 'current-password'
    }))

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autocomplete': 'email'
        })
    )
    terms = forms.BooleanField(
        required=True,
        label="I agree to the Terms of Service and Privacy Policy"
    )
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose a username',
        'autocomplete': 'username'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Create a password',
        'autocomplete': 'new-password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm your password',
        'autocomplete': 'new-password'
    }))

    class Meta(UserCreationForm.Meta):
        model = UserCreationForm.Meta.model
        fields = ("username", "email", "password1", "password2", "terms")

    def clean_terms(self):
        terms = self.cleaned_data.get('terms')
        if not terms:
            raise forms.ValidationError("You must agree to the Terms of Service and Privacy Policy.")
        return terms 