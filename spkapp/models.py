from django.db import models
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, default='NA')

    def __str__(self):
        return self.name


class order_model(models.Model):
    status = (('Draft', 'Draft'), ('Approved', 'Approved'),)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    projects = (
        ('Siltronics - External Works', 'Siltronics - External Works'),
    )

    requester = models.CharField(max_length=40)
    projectname = models.CharField(max_length=30, choices=projects)
    approver = models.CharField(max_length=40)
    # status = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=status, default='Draft')
    quantity = models.IntegerField()
    remarks = models.TextField()
    order_date = models.DateTimeField(default=timezone.now)
    approved_date = models.DateField(auto_now=True)


def __str__(self):
    return 'Emp details shared'
