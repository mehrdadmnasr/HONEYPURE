from django.db import models

class Translation(models.Model):
    original_text = models.TextField()  # متن اصلی
    language = models.CharField(max_length=10)  # زبان ترجمه
    translated_text = models.TextField()  # متن ترجمه شده

    def __str__(self):
        return f"{self.original_text[:50]} - {self.language}"
