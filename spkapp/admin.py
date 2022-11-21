from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import order_model, Category, Product, Projects, Units, Vendor
# Register your models here.

admin.site.register(order_model)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Projects)
admin.site.register(Units)
admin.site.register(Vendor)


