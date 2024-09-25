from django.core.management.base import BaseCommand
from translation.utils import load_translations

class Command(BaseCommand):
    help = 'Load all translations from .po files into the database'

    def handle(self, *args, **kwargs):
        load_translations()
        self.stdout.write(self.style.SUCCESS('Translations loaded successfully!'))
