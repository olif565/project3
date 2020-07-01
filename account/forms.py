from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

STATUS_CHOICES = (
        ('', '--Pilih Status--'),
        (True, 'ADMIN'),
        (False, 'STAFF')
    )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=30,
                                 widget=forms.TextInput())
    last_name = forms.CharField(label='Last Name', max_length=150,
                                widget=forms.TextInput())
    username = forms.CharField(label='Username', max_length=50,
                               widget=forms.TextInput())
    email = forms.CharField(label='Email', max_length=50,
                            widget=forms.TextInput())
    password1 = forms.CharField(label='Password', max_length=30,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password Confirmation', max_length=30,
                                widget=forms.PasswordInput())
    is_staff = forms.ChoiceField(label='Status', choices=STATUS_CHOICES)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'is_staff')


class SignUpFormUser(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=30,
                                 widget=forms.TextInput())
    last_name = forms.CharField(label='Last Name', max_length=150,
                                widget=forms.TextInput())
    username = forms.CharField(label='Username', max_length=50,
                               widget=forms.TextInput())
    email = forms.CharField(label='Email', max_length=50,
                            widget=forms.TextInput())
    password1 = forms.CharField(label='Password', max_length=30,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password Confirmation', max_length=30,
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=20,
                               widget=forms.TextInput())
    password = forms.CharField(label='Password', max_length=20,
                               widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')
