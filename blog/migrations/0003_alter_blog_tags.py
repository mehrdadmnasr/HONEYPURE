# Generated by Django 5.1 on 2024-08-29 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='tags',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
