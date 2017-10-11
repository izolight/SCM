from django.db import models
from django.core.validators import RegexValidator


class Member(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.ForeignKey(City, related_name='members')
    phone_regex = RegexValidator(regex=r'^\+41\d{9}$', message="Bitte gültige Telefonnummer eingeben")
    phone_number = models.CharField(validators=[phone_regex], max_length=12)
    email = models.EmailField(max_length=200)
    user_name = models.CharField(max_length=50, unique=True)  # TODO connect with builtin auth
    website = models.URLField(max_length=100, blank=True)


class City (models.Model):
    zip_regex = RegexValidator(regex=r'^\d{4}$', message="Bitte vierstellige PLZ eingeben")
    zip_code = models.PositiveSmallIntegerField(validators=[zip_regex], unique=True)
    city = models.CharField(max_length=30)
