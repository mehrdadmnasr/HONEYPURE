# Generated by Django 5.1 on 2024-09-09 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_alter_address_address_details_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_details',
            field=models.TextField(blank=True, null=True),
        ),
    ]