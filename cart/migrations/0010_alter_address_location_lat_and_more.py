# Generated by Django 5.1 on 2024-09-15 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_alter_address_address_details_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='location_lat',
            field=models.DecimalField(decimal_places=18, max_digits=22),
        ),
        migrations.AlterField(
            model_name='address',
            name='location_long',
            field=models.DecimalField(decimal_places=18, max_digits=22),
        ),
    ]
