from django.contrib import admin
from .models import order_model, Category, Product, Projects, Units
# Register your models here.

admin.site.register(order_model)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Projects)
admin.site.register(Units)

