from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewMemberForm(UserCreationForm):
    address = forms.CharField()
    city = forms.CharField()
    zip_code = forms.IntegerField()
    phone_number = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',
                  'address', 'city', 'zip_code', 'phone_number')
