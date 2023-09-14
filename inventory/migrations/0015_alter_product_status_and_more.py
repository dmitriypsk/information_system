# Generated by Django 4.1.7 on 2023-05-01 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_creditsale__remaining_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('На складе', 'На складе'), ('Продан', 'Продан'), ('Списан', 'Списан'), ('Возвращен', 'Возвращен')], default='На складе', max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('Продажа', 'Продажа'), ('Возврат', 'Возврат'), ('Списание', 'Списание')], max_length=50, verbose_name='Тип операции'),
        ),
    ]