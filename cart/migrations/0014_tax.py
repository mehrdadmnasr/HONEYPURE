# Generated by Django 5.1 on 2024-09-17 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_remove_coupon_discount_cartitem_tax_percent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(default=2024)),
                ('tax_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('toll_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]