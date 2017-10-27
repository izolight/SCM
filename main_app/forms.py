from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class NewMemberForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    address = forms.CharField(max_length=50, label="Address")
    city = forms.CharField(max_length=30, label="City")
    zip_code = forms.RegexField(regex=r'^\d{4}$', label="Zip Code",
                                error_messages={'invalid': 'Bitte eine vierstellige Postleitzahl eingeben!'})
    phone_number = forms.RegexField(regex=r'^\+41\d{9}$', label="Phone Number", initial="+41",
                                    error_messages={'invalid': 'Enter a valid phone number'})
    email = forms.EmailField(label="E-Mail Address")
    username = forms.RegexField(regex=r'^[a-zA-Z][a-zA-Z0-9]{1,19}$', label="Username", error_messages={
        'invalid': "Usernames are without punctuation marks. It contains one to twenty characters. Please, don't use 'ä', 'ö' and 'ü'"})
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password", min_length=10)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm password", min_length=10)

    def clean(self):
        cleaned_data = super(NewMemberForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error('password2', "Passwords do not match")
