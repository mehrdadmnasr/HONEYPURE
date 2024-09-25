from django.contrib import admin
from .models import Translation

class TranslationAdmin(admin.ModelAdmin):
    list_display = ('original_text', 'language', 'translated_text')
    list_filter = ('language',)
    search_fields = ('original_text', 'translated_text')
    fields = ('original_text', 'language', 'translated_text')  # تعیین ترتیب فیلدها

admin.site.register(Translation, TranslationAdmin)
