"""
forms.py: hold all forms classes which will give over to related views
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from datetime import datetime, timedelta

from main_app.models import IceSlot, Training, Member, Club, Invoice


class AddMemberForm(forms.Form):
    """
    Form for new member with specified user input checks.
    """
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
        'invalid': "Usernames are without punctuation marks. It contains one to twenty characters. Please, don't use "
                   "'ä', 'ö' and 'ü'"})
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password", min_length=10)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm password", min_length=10)

    def clean(self):
        """
        logic for own user input checks
        """
        cleaned_data = super(AddMemberForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error('password2', "Passwords do not match")


class EditMemberForm(forms.Form):
    """
    Form for editing Member, not all values can be edited
    """
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    address = forms.CharField(max_length=50, label="Address")
    city = forms.CharField(max_length=30, label="City")
    zip_code = forms.RegexField(regex=r'^\d{4}$', label="Zip Code",
                                error_messages={'invalid': 'Bitte eine vierstellige Postleitzahl eingeben!'})
    phone_number = forms.RegexField(regex=r'^\+41\d{9}$', label="Phone Number", initial="+41",
                                    error_messages={'invalid': 'Enter a valid phone number'})

    def __init__(self, *args, **kwargs):
        super().__init__()
        member = kwargs['member']
        self.first_name = member.user.first_name
        self.last_name = member.user.last_name
        self.address = member.address
        self.city = member.city.name
        self.zip_code = member.city.zip_code
        self.phone_number = member.phone_number


class CreateInvoiceForm(forms.ModelForm):
    """
    Form to create an invoice
    """
    due_date = forms.DateTimeField(initial=datetime.now() + timedelta(days=30))
    create_date = forms.DateTimeField(initial=datetime.now())

    class Meta:
        """
        Automatically creates form field with defined attributes of class Invoice
        """
        model = Invoice
        fields = ('title', 'description', "amount", "due_date", "member", "create_date")

    def clean(self):
        """
        Special check ...
        """
        cleaned_data = super(CreateInvoiceForm, self).clean()

    def __init__(self, *args, **kwargs):
        super().__init__()
        club = kwargs['club']
        self.member = forms.ModelChoiceField(queryset=Member.objects.filter(club=club))


class SignUpForm(UserCreationForm):
    """
    Form for users who like to sign up for application
    """
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        """
        Automatically creates form field with defined attributes of class User
        """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class AddIceForm(forms.ModelForm):
    """
    Form to add an ice time slot
    """
    start_time = forms.DateTimeField(initial=datetime.now)
    end_time = forms.DateTimeField(initial=datetime.now() + timedelta(hours=1))

    class Meta:
        """
        Automatically creates form field with defined attributes of class IceSlot
        """
        model = IceSlot
        fields = ('start_time', 'end_time',)

    def clean(self):
        """
        Special check whether the ice slot is not overlapping nor that is has bad input
        such as start time is before end time
        """
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
            if i.id != self.instance.id:
                if i.start_time <= start_time < i.end_time:
                    self.add_error('start_time',
                               f"There is already a slot between {i.start_time: %H:%M} - {i.end_time: %H:%M}")
                if i.start_time < end_time <= i.end_time:
                    self.add_error('end_time',
                               f"There is already a slot between {i.start_time: %H:%M} - {i.end_time: %H:%M}")


class AddTrainingForm(forms.ModelForm):
    """
    Form to add a training to an ice slot
    """
    start_time = forms.DateTimeField(initial=datetime.now)
    end_time = forms.DateTimeField(initial=datetime.now() + timedelta(hours=1))

    class Meta:
        """
        Automatically creates form field with defined attributes of class Training
        """
        model = Training
        fields = ['title', 'description', 'start_time', 'end_time',
                  'members', 'trainer', 'ice_slot']

    def __init__(self, *args, **kwargs):
        super().__init__()
        club = kwargs['club']
        self.members = forms.ModelMultipleChoiceField(queryset=Member.objects.filter(club=club))
        self.trainer = forms.ModelChoiceField(queryset=Member.objects.filter(club=club))
        self.ice_slot = forms.ModelChoiceField(queryset=IceSlot.objects.filter(club=club))
