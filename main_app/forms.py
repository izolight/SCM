"""
forms.py: hold all forms classes which will give over to related views
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy

from datetime import datetime, timedelta

from main_app.models import IceSlot, Training, Member, Club, Invoice


class AddMemberForm(forms.Form):
    """
    Form for new member with specified user input checks.
    """
    first_name = forms.CharField(max_length=30, label=gettext_lazy("First Name"))
    last_name = forms.CharField(max_length=30, label=gettext_lazy("Last Name"))
    address = forms.CharField(max_length=50, label=gettext_lazy("Address"))
    city = forms.CharField(max_length=30, label=gettext_lazy("City"))
    zip_code = forms.RegexField(regex=r'^\d{4}$', label=gettext_lazy("Zip Code"),
                                error_messages={'invalid': gettext_lazy("Enter correct Zip Code")})
    phone_number = forms.RegexField(regex=r'^\+41\d{9}$', label=gettext_lazy("Phone Number"), initial="+41",
                                    error_messages={'invalid': gettext_lazy("Enter a valid phone number")})
    email = forms.EmailField(label=gettext_lazy("E-Mail address"))
    username = forms.RegexField(regex=r'^[a-zA-Z][a-zA-Z0-9]{1,19}$', label=gettext_lazy("Username"), error_messages={
        'invalid': gettext_lazy(
            "Usernames are without punctuation marks. It contains one to twenty characters. Please, don't use "
            "'ä', 'ö' and 'ü'")})
    club = forms.ModelChoiceField(queryset=Club.objects.all())
    password1 = forms.CharField(widget=forms.PasswordInput(), label=gettext_lazy("Password"), min_length=10)
    password2 = forms.CharField(widget=forms.PasswordInput(), label=gettext_lazy("Confirm Password"), min_length=10)

    def clean(self):
        """
        logic for own user input checks
        """
        cleaned_data = super(AddMemberForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error('password2', gettext_lazy("Passwords do not match"))


class EditMemberForm(forms.Form):
    """
    Form for editing Member, not all values can be edited
    """
    first_name = forms.CharField(max_length=30, label=gettext_lazy("First Name"))
    last_name = forms.CharField(max_length=30, label=gettext_lazy("Last Name"))
    address = forms.CharField(max_length=50, label=gettext_lazy("Address"))
    city = forms.CharField(max_length=30, label=gettext_lazy("City"))
    zip_code = forms.RegexField(regex=r'^\d{4}$', label=gettext_lazy("Zip Code"),
                                error_messages={'invalid': gettext_lazy("Enter correct Zip Code")})
    phone_number = forms.RegexField(regex=r'^\+41\d{9}$', label=gettext_lazy("Phone Number"), initial="+41",
                                    error_messages={'invalid': gettext_lazy("Enter a valid phone number")})
    email = forms.EmailField(label=gettext_lazy("E-Mail address"))

    def __init__(self, *args, **kwargs):
        member = kwargs.pop('member')
        super().__init__(*args, **kwargs)
        self.initial["first_name"] = member.user.first_name
        self.initial["last_name"] = member.user.last_name
        self.initial["address"] = member.address
        self.initial["city"] = member.city.name
        self.initial["zip_code"] = member.city.zip_code
        self.initial["phone_number"] = member.phone_number
        self.initial["email"] = member.user.email


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
    email = forms.EmailField(max_length=254, help_text=gettext_lazy("Enter a valid email address."))

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
            self.add_error('end_time', gettext_lazy("End Time can't be before Start Time"))

        if start_time.date() != end_time.date():
            self.add_error('end_time', gettext_lazy("End Time must be on the same day as Start Time"))

        ice_slots = IceSlot.objects.filter(start_time__day=start_time.day,
                                           start_time__month=start_time.month,
                                           start_time__year=start_time.year)
        for i in ice_slots:
            if i.id != self.instance.id:
                if i.start_time <= start_time < i.end_time:
                    self.add_error('start_time',
                                   gettext_lazy("There is already a slot between {start: %H:%M} - {end: %H:%M}").format(
                                       start=i.start_time, end=i.end_time))
                if i.start_time < end_time <= i.end_time:
                    self.add_error('end_time',
                                   gettext_lazy("There is already a slot between {start: %H:%M} - {end: %H:%M}").format(
                                       start=i.start_time, end=i.end_time))


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
        club = kwargs.pop('club')
        super().__init__(*args, **kwargs)
        self.members = forms.ModelMultipleChoiceField(queryset=Member.objects.filter(club=club))
        self.trainer = forms.ModelChoiceField(queryset=Member.objects.filter(club=club))
        self.ice_slot = forms.ModelChoiceField(queryset=IceSlot.objects.filter(club=club))
