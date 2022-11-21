from email.policy import default
from django.db import models
from django.utils import timezone


# Create your models here.
class Projects(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Units(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # name = models.CharField(max_length=40, default='NA')
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class order_model(models.Model):
    orderno = models.CharField(max_length=10, default='SPK-00001')
    status = (('Requested', 'Requested'), ('Checked', 'Checked'), ('Approved', 'Approved'), ('Rejected', 'Rejected'),)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    requester = models.CharField(max_length=40)
    projectname = models.ForeignKey(Projects, on_delete=models.SET_NULL, blank=True, null=True)
    approver = models.CharField(max_length=40)
    status = models.CharField(max_length=10, choices=status, default='Requested')
    quantity = models.IntegerField()
    unit = models.ForeignKey(Units, on_delete=models.SET_NULL, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)
    order_date = models.DateField(auto_now_add=True, auto_now=False)
    approved_date = models.DateField(auto_now=True)

    def __str__(self):
        return 'Order details shared'
