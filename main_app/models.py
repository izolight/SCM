from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class City(models.Model):
    zip_regex = RegexValidator(regex=r'^\d{4}$', message="Bitte vierstellige PLZ eingeben")
    zip_code = models.PositiveSmallIntegerField(validators=[zip_regex])
    city = models.CharField(max_length=30)


class Member(models.Model):
    address = models.CharField(max_length=50, null=True)
    city = models.ForeignKey(City, related_name='member', null=True)
    phone_regex = RegexValidator(regex=r'^\+41\d{9}$', message="Bitte gültige Telefonnummer eingeben")
    phone_number = models.CharField(validators=[phone_regex], max_length=12, null=True)
    user_name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    website = models.URLField(max_length=100, blank=True, null=True)


# see https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
@receiver(post_save, sender=User)
def create_member(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user_name=instance)


@receiver(post_save, sender=User)
def save_member(sender, instance, **kwargs):
    instance.member.save()