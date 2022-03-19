from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=(("1", "Doctor"), ("2", "Patient")), required=True)

    class Meta:
        model = User
        fields = ('role', 'username', 'password1', 'password2')


class Prescription(forms.Form):
    file = forms.FileField(required=True)
    privateKey = forms.CharField(max_length=64, required=True)
    publicKey = forms.CharField(max_length=64, required=True)
