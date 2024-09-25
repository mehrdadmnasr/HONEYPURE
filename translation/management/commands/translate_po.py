from django.core.management.base import BaseCommand
from googletrans import Translator
import polib
import os
import time

class Command(BaseCommand):
    help = 'Translate PO files using Google Translate'

    def handle(self, *args, **kwargs):
        languages = ['fa', 'en', 'fr', 'tr']
        translator = Translator()

        for lang in languages:
            po_file_path = f'locale/{lang}/LC_MESSAGES/django.po'
            if os.path.exists(po_file_path):
                po_file = polib.pofile(po_file_path)

                for entry in po_file.untranslated_entries():
                    translated_text = None
                    attempts = 0
                    max_attempts = 5

                    while attempts < max_attempts:
                        try:
                            translated_text = translator.translate(entry.msgid, dest=lang).text
                            break
                        except Exception as e:
                            attempts += 1
                            print(f'Error translating "{entry.msgid}": {e}')
                            time.sleep(2)

                    if translated_text:
                        entry.msgstr = translated_text
                        print(f'Translated "{entry.msgid}" to "{translated_text}" in {lang}')
                    else:
                        print(f'Failed to translate "{entry.msgid}" after {max_attempts} attempts.')

                po_file.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully translated {lang} po file!'))
