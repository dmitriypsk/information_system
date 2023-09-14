from django import forms
from django.core.exceptions import ValidationError
from django_select2.forms import ModelSelect2Widget, Select2Widget, Select2MultipleWidget
from .models import Product, Category, Supplier, Transaction, CreditSale, CreditPayment
from django.db.models import Q
from django_countries.widgets import CountrySelectWidget
from django.forms import TextInput, Textarea


class ProductSKUChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.sku


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'sku', 'name', 'country_of_manufacture','manufacturer', 'supplier', 'gender',
            'category', 'date_received', 'purchase_price', 'sale_price',
            'discounted_price', 'size', 'color'
        ]
        widgets = {
            'country_of_manufacture': CountrySelectWidget(),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.groups.filter(name="Продавец").exists():
            self.fields['purchase_price'].widget = forms.HiddenInput()
            self.fields['supplier'].widget = forms.HiddenInput()


    def clean(self):
        cleaned_data = super().clean()
        sku = cleaned_data.get('sku')

        if self.instance.pk:  # Если товар редактируется, исключаем его из проверки
            if Product.objects.exclude(pk=self.instance.pk).filter(sku=sku).exists():
                raise ValidationError("Товар с таким артикулом уже существует.")
        else:  # Если товар создается
            if Product.objects.filter(sku=sku).exists():
                raise ValidationError("Товар с таким артикулом уже существует.")
        return cleaned_data
    

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'address', 'contact_info']
        labels = {
            'name': 'Название компании',
            'address': 'Адрес',
            'contact_info': 'Контакты',
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:50%'}),
            'address': Textarea(attrs={'class': 'form-control', 'style': 'width:50%; height: 100px;'}),
            'contact_info': Textarea(attrs={'class': 'form-control', 'style': 'width:50%; height: 100px;'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:50%'}),
            'description': Textarea(attrs={'class': 'form-control', 'style': 'width:50%; height: 100px;'}),
        }


class TransactionForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        label='Товары',
        widget=Select2MultipleWidget(attrs={'style': 'width: 100%;'}),
        to_field_name='sku',
    )

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'products']
        widgets = {
            'transaction_type': Select2Widget(attrs={'style': 'width: 100%;'}),
        }

        
class CreditSaleForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(Q(creditsale__isnull=True) | Q(creditsale__settled=True), status=Product.IN_STOCK).exclude(id__in=Transaction.objects.filter(transaction_type='sale').values('products')),
        label='Товары',
        widget=Select2MultipleWidget(
            attrs={
                'data-minimum-input-length': 0,
                'data-placeholder': 'Выберите товары',
                'style': 'width: 100%'
            }
        ),
    )

    class Meta:
        model = CreditSale
        fields = [
            'contract_number', 'products', 'customer_name', 'customer_phone', 'customer_email', 'sale_date', 'total_price', 'down_payment', 'credit_months', 'monthly_payment'
        ]
        labels = {
            'contract_number': 'Номер договора',
            'products': 'Товары',
            'customer_name': 'Имя покупателя',
            'customer_phone': 'Телефон покупателя',
            'customer_email': 'Email покупателя',
            'sale_date': 'Дата продажи',
            'total_price': 'Общая сумма',
            'down_payment': 'Первоначальный взнос',
            'credit_months': 'Срок (месяцев)',
            'monthly_payment': 'Ежемесячный платеж',
        }


class CreditPaymentForm(forms.ModelForm):
    class Meta:
        model = CreditPayment
        fields = [ 'payment_date', 'amount']
        labels = {
            'payment_date': 'Дата платежа',
            'amount': 'Сумма платежа',
            
        }
        widgets = {
            'credit_sale': ModelSelect2Widget(),
        }
