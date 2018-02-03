from django import forms
from django.core.exceptions import ValidationError


class AuthorizationForm(forms.Form):
    pnum = forms.CharField(label="Pnum")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    name = forms.CharField(label="Name")
    surname = forms.CharField(label="Surname")
    pnum = forms.CharField(label="Phone")
    address = forms.CharField(label="Adress")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Repeat password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')

        if password != password_repeat:
            self.add_error(
                'password_repeat',
                "Passwords must be the same"
            )

        return cleaned_data