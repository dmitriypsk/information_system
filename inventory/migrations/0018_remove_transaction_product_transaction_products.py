# Generated by Django 4.1.7 on 2023-05-02 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_alter_creditsale_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='product',
        ),
        migrations.AddField(
            model_name='transaction',
            name='products',
            field=models.ManyToManyField(to='inventory.product', verbose_name='Товары'),
        ),
    ]
