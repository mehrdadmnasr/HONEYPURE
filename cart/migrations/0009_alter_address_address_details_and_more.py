# Generated by Django 5.1 on 2024-09-09 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_alter_address_address_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_details',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='address',
            name='location_lat',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='address',
            name='location_long',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
    ]
