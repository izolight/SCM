"""
models.py: responsible for defining all model classes.
Django also uses this class to create a database model.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy


class City(models.Model):
    """
    Class City: with specified type checks like zip must be 4 digits
    """
    zip_regex = RegexValidator(regex=r'^\d{4}$', message=gettext_lazy("Enter correct Zip Code"))
    zip_code = models.PositiveSmallIntegerField(validators=[zip_regex])
    name = models.CharField(max_length=30)


class Club(models.Model):
    """
    Class Club: defines club name and description.
    """
    name = models.CharField(max_length=50)
    description = models.TextField()


class Member(models.Model):
    """
    Class Member: linked to django default user Class to extend user attributes.
    """
    address = models.CharField(max_length=50, null=True)
    city = models.ForeignKey(City, related_name='members', null=True)
    phone_regex = RegexValidator(regex=r'^\+41\d{9}$', message=gettext_lazy("Enter a valid phone number"))
    phone_number = models.CharField(validators=[phone_regex], max_length=12, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    website = models.URLField(max_length=100, blank=True, null=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, related_name="members")

    def __str__(self):
        """
        Overwriting to string method (otherwise it returns just the whole object of Member)
        :return: formatted member name string in format: first name + last name
        """
        return f'{self.user.first_name} {self.user.last_name}'


@receiver(post_save, sender=User)
def create_member(sender, instance, created, **kwargs):
    """
    Hooking the create_member and save_member methods to the User model
    """
    if created:
        Member.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_member(sender, instance, **kwargs):
    """
    Hooking the create_member and save_member methods to the User model
    """
    instance.member.save()


class Invoice(models.Model):
    """
    Class Invoice: Defines a invoice
    """
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)
    amount = models.IntegerField()
    due_date = models.DateField()
    create_date = models.DateField()
    paid_date = models.DateField(null=True)
    canceled = models.BooleanField(default=False)
    member = models.ForeignKey(Member, on_delete=models.PROTECT, related_name="invoices")

    def __str__(self):
        """
        Overwriting to string method (otherwise it returns just the whole object of Invoice)
        :return: string title of invoice string
        """
        return self.title


class IceSlot(models.Model):
    """
    Class IceSlot: hold start and end time of an ice slot and it links to which club it belongs
    """
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, related_name="ice_slots")

    def __str__(self):
        """
        Overwriting to string method (otherwise it returns just the whole object of IceSlot)
        :return: string in format: ice slot start time and ice slot end time
        """
        return f'{self.start_time} - {self.end_time}'


class Training(models.Model):
    """
    Class Training: Holds all needed training information, like who is the trainer and players
    and links it to an ice slot.
    """
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    members = models.ManyToManyField(Member, related_name="trainings")
    trainer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name="trainings_as_trainer")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, related_name="trainings")
    ice_slot = models.ForeignKey(IceSlot, on_delete=models.SET_NULL, null=True, related_name="trainings")

    def __str__(self):
        """
        Overwriting to string method (otherwise it returns just the whole object of Training)
        :return: title of training string
        """
        return self.title


class SubscriptionType(models.Model):
    """
    Class SubscriptionType: gives a choice of different invoice subscription types.
    like: member fee, training camp, material sell, etc.
    """
    name = models.CharField(max_length=50)


class Subscription(models.Model):
    """
    Class Subscription: binds the invoice with subscriptions and their type.
    """
    type = models.ForeignKey(SubscriptionType, on_delete=models.SET_NULL, null=True, related_name="subscriptions")
    price = models.IntegerField()
    duration = models.IntegerField()
    description = models.TextField()
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, related_name="subscriptions")
