# Generated by Django 4.1.7 on 2023-04-22 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_creditsale_creditpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditsale',
            name='settled',
            field=models.BooleanField(default=False),
        ),
    ]
