
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import accounts
from django import forms


class sign_up(UserCreationForm):
    class Meta:
        model = accounts
        fields = ['first_name', 'last_name',
                  'idnumber', 'email', 'contactnumber', 'username','course','year','birthday','usertype','password1', 'password2']