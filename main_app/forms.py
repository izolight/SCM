from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from main_app.models import IceSlot


class AddMemberForm(forms.Form):
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
        cleaned_data = super(AddMemberForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error('password2', "Passwords do not match")


class CreateInvoiceForm(forms.Form):
    title = forms.CharField(max_length=50, label="Title")
    description = forms.CharField(widget=forms.Textarea())
    amount = forms.IntegerField(None, 1)
    due_date = forms.DateField()


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class AddIceForm(forms.ModelForm):
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()

    class Meta:
        model = IceSlot
        fields = ('start_time', 'end_time',)

    def clean(self):
        cleaned_data = super(AddIceForm, self).clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if end_time <= start_time:
            self.add_error('end_time', "Must be greater than start")

        if start_time.date() != end_time.date():
            self.add_error('end_time', "Must be on the same day as start")

        ice_slots = IceSlot.objects.filter(start_time__day=start_time.day,
                                           start_time__month=start_time.month,
                                           start_time__year=start_time.year)
        for i in ice_slots:
            if start_time >= i.start_time and start_time < i.end_time:
                self.add_error('start_time',
                               f"There is already a slot between {i.start_time: %H:%M} - {i.end_time: %H:%M}")
            if end_time > i.start_time and end_time <= i.end_time:
                self.add_error('end_time',
                               f"There is already a slot between {i.start_time: %H:%M} - {i.end_time: %H:%M}")
