from django.core.management.base import BaseCommand
from main_app.models import *


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_clubs(self):
        c1 = Club(name='Testclub', description='For tests')
        c1.save()
        c2 = Club(name='Der Klub', description='for the lulz')
        c2.save()
        c3 = Club(name='Fancy Club', description='very fancy')
        c3.save()

    def handle(self, *args, **options):
        self._create_clubs()