from django.db import models
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from django_countries.fields import CountryField


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    GENDER_CHOICES = (
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
        ('У', 'Унисекс'),
    )
    gender = models.CharField("Гендер",max_length=1, choices=GENDER_CHOICES, default='У')
    name = models.CharField("Название",max_length=100)
    sku = models.CharField("Артикул",max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    manufacturer = models.CharField("Фирма",max_length=100)
    country_of_manufacture = CountryField(blank_label='Выберите страну', verbose_name='Страна производителя', null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Поставщик')
    date_received = models.DateField("Дата поступления",default=timezone.now)
    purchase_price = models.DecimalField("Цена закупки",max_digits=10, decimal_places=2, default=0)
    sale_price = models.DecimalField("Цена",max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField("Цена со скидкой",max_digits=10, decimal_places=2, null=True, blank=True)
    size = models.CharField("Размер", max_length=50, default='0')
    color = models.CharField("Цвет", max_length=50, default='не задан')

    IN_STOCK = 'in_stock'
    SOLD = 'sold'
    WRITTEN_OFF = 'written_off'

    STATUS_CHOICES = [
        (IN_STOCK, 'На складе'),
        (SOLD, 'Продан'),
        (WRITTEN_OFF, 'Списан'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=IN_STOCK,
    )

    def __str__(self):
        return f"{self.sku} - {self.name}"


class InventoryItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)


class CreditSale(models.Model):
    products = models.ManyToManyField(Product, verbose_name='Товары')
    contract_number = models.CharField(max_length=20, unique=True,default=0)
    customer_name = models.CharField(max_length=100,default=0)
    customer_phone = models.CharField(max_length=15,default=0)
    customer_email = models.EmailField(default=0)
    sale_date = models.DateField()
    total_price = models.IntegerField()
    down_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit_months = models.PositiveIntegerField(default=12)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    settled = models.BooleanField(default=False)
    _remaining_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    def save(self, *args, **kwargs):
        self.total_price = Decimal(self.total_price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        super(CreditSale, self).save(*args, **kwargs)

    @property
    def remaining_amount(self):
        return self._remaining_amount

    @remaining_amount.setter
    def remaining_amount(self, value):
        self._remaining_amount = value


class CreditPayment(models.Model):
    credit_sale = models.ForeignKey(CreditSale, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)  # Добавьте это поле

    def __str__(self):
        return f"{self.credit_sale.contract_number} - {self.payment_date}"


class Transaction(models.Model):
    SALE = 'SALE'
    RETURN = 'RETURN'
    WRITE_OFF = 'WRITE_OFF'

    TRANSACTION_TYPES = [
        (SALE, 'Продажа'),
        (RETURN, 'Возврат'),
        (WRITE_OFF, 'Списание'),
    ]

    created_at = models.DateTimeField(default=timezone.now)
    products = models.ManyToManyField(Product, verbose_name='Товары')
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES, verbose_name='Тип операции')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата операции')
    total_price = models.FloatField(null=True, blank=True, verbose_name='Общая сумма')
    credit_sale = models.ForeignKey(CreditSale, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Кредитная продажа')

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
