# Generated by Django 5.1 on 2024-08-12 21:05

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='description',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
