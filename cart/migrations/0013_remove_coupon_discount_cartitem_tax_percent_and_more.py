# Generated by Django 5.1 on 2024-09-16 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_address_unique_address_name_per_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='discount',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='tax_percent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='toll_percent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
