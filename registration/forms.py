from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    photo = forms.ImageField(label='Картинка пользователя')

class UserProfileForm(forms.Form):
    login = forms.CharField(max_length=30, label='Логин', disabled=True, required=False)
    email = forms.EmailField(widget=forms.EmailInput)
    photo = forms.ImageField(label='Картинка пользователя', required=False)



