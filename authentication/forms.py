from django import forms


class AuthorizationForm(forms.Form):
    pnum = forms.CharField(label="Pnum")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegistrationForm(forms.Form):

    USER_TYPES = (
        ('Student', 'Student'),
        ('Professor', 'Professor'),
        ('Instructor', 'Instructor'),
        ('Admin', 'Admin'),
        ('TA', 'TA'),
        ('VisitingProfessor', 'Visiting Professor'),
        ('Librarian', 'Librarian'),
    )

    name = forms.CharField(label="Name", required=True)
    surname = forms.CharField(label="Surname", required=True)
    address = forms.CharField(label="Adress", required=True)
    pnum = forms.CharField(label="Phone", required=True)
    password = forms.CharField(label="Password", required=True, widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Repeat password", required=True, widget=forms.PasswordInput)
    user_type = forms.ChoiceField(label='Who are you?', required=True, widget=forms.Select, choices=USER_TYPES)

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
