from django import forms
from django.forms import ModelForm
from .models import order_model, Category, Product


# create a order form

class order_form(ModelForm):
    class Meta:
        model = order_model
        fields = ('projectname', 'category', 'product', 'quantity', 'remarks', 'order_date', 'status')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['product'].queryset = Product.objects.none()

            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['product'].queryset = Product.objects.filter(category_id=category_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['product'].queryset = self.instance.category.product_set.order_by('name')
