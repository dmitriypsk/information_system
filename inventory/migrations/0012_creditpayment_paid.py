# Generated by Django 4.1.7 on 2023-04-29 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_creditsale_settled'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditpayment',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
