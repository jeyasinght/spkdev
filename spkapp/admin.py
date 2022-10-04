from django.contrib import admin
from .models import order_model, Category, Product
# Register your models here.

admin.site.register(order_model)
admin.site.register(Category)
admin.site.register(Product)

