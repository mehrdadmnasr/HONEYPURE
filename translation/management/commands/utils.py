import polib
import os
from django.core.management.base import BaseCommand
from translation.models import Translation

def load_translations():
    languages = ['fa', 'en', 'fr', 'tr']

    for lang in languages:
        po_file_path = f'locale/{lang}/LC_MESSAGES/django.po'
        if os.path.exists(po_file_path):
            po_file = polib.pofile(po_file_path)

            for entry in po_file:
                if not Translation.objects.filter(original_text=entry.msgid, language=lang).exists():
                    Translation.objects.create(
                        original_text=entry.msgid,
                        language=lang,
                        translated_text=entry.msgstr
                    )

class Command(BaseCommand):
    help = 'Load translations from .po files into the database'

    def handle(self, *args, **kwargs):
        load_translations()
        self.stdout.write(self.style.SUCCESS('Translations loaded successfully!'))
