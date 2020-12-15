from django import forms
from .models import User


class AuthForm(forms.Form):
    username = User.username
    password = User.password


class RegForm(forms.Form):
    username = User.username
    password = User.password
    repeat_password = User.password
