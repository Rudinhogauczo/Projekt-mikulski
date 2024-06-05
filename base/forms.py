from django import forms
from .models import Urzadzenie
from django.contrib.auth.forms import AuthenticationForm
class DeviceForm(forms.ModelForm):
    class Meta:
        model = Urzadzenie
        fields = ['name', 'room', 'state']


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields['username'].label=False
        self.fields['password'].label=False
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Hasło'})
    error_messages = {
        "invalid_login": "Nieprawidłowy login lub hasło",
    }

class RoomForm(forms.Form):
    nazwa_pokoju = forms.CharField(max_length=100)
    opis_pokoju = forms.CharField(max_length=200)


class UrzadzenieForm(forms.ModelForm):
    class Meta:
        model = Urzadzenie
        fields = ['name', 'room', 'pin']