from django.contrib import admin

from .models import Product, Category, Card, Cart

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Card)

