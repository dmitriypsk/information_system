# Generated by Django 4.1.7 on 2023-05-01 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_rename_total_amount_creditsale_total_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditsale',
            name='_remaining_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
