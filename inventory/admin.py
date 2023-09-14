from django.contrib import admin
from inventory.models import Product, Category, Supplier, Transaction, CreditSale, CreditPayment, InventoryItem

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Transaction)
admin.site.register(CreditSale)
admin.site.register(CreditPayment)
admin.site.register(InventoryItem)