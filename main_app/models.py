from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class City(models.Model):
    zip_regex = RegexValidator(regex=r'^\d{4}$', message="Bitte vierstellige PLZ eingeben")
    zip_code = models.PositiveSmallIntegerField(validators=[zip_regex])
    name = models.CharField(max_length=30)


class Member(models.Model):
    address = models.CharField(max_length=50, null=True)
    city = models.ForeignKey(City, related_name='members', null=True)
    phone_regex = RegexValidator(regex=r'^\+41\d{9}$', message="Bitte gültige Telefonnummer eingeben")
    phone_number = models.CharField(validators=[phone_regex], max_length=12, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    website = models.URLField(max_length=100, blank=True, null=True)


# see https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=User)
def create_member(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user_name=instance)


@receiver(post_save, sender=User)
def save_member(sender, instance, **kwargs):
    instance.member.save()


class Invoice(models.Model):
    number = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    amount = models.IntegerField()
    due_date = models.DateField()
    create_date = models.DateField()
    paid_date = models.DateField()
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)


class Club(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    members = models.ManyToManyField(Member)


class IceSlot(models.Model):
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True)


class Training(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    members = models.ManyToManyField(Member, related_name="trainings")
    trainer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name="trainings_as_trainer")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, related_name="trainings")
    ice_slot = models.OneToOneField(IceSlot, on_delete=models.SET_NULL, null=True)


class SubscriptionType(models.Model):
    name = models.CharField(max_length=50)


class Subscription(models.Model):
    type = models.ForeignKey(SubscriptionType, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    duration = models.IntegerField()
    description = models.TextField()
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)