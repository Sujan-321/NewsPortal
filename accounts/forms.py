from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class":"form-control", "placeholder":"Enter Your Email"}
        ),
    )


    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={"class":"form-control", "placeholder":"Choose Username"}
        ),

    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
             attrs={"class":"form-control", "placeholder":"Enter Password"}
        ),
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(
             attrs={"class":"form-control", "placeholder":"Confirm Password"}
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = {"username", "email"}
    
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class":"form-control", "placeholder":"Username"}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class":"form-control", "placeholder":"Password"}
        )
    )
